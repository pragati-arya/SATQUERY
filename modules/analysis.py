from PIL import Image, ImageFilter
import numpy as np


def arr(image):
    return np.asarray(
        image.convert("RGB"),
        dtype=np.float32
    )


def smooth(image, radius=2):
    a = arr(image)

    im = Image.fromarray(
        np.clip(a, 0, 255).astype(np.uint8)
    ).filter(
        ImageFilter.GaussianBlur(radius)
    )

    return np.asarray(
        im,
        dtype=np.float32
    )


def adaptive_threshold(values, percentile=93, minimum=0.06):
    v = values[np.isfinite(values)]

    if v.size == 0:
        return minimum

    return max(
        float(np.percentile(v, percentile)),
        minimum
    )


def clean_mask(mask, min_size=30):
    im = (
        Image.fromarray(
            mask.astype(np.uint8) * 255
        )
        .filter(ImageFilter.MaxFilter(5))
        .filter(ImageFilter.MinFilter(5))
    )

    mask = np.asarray(im) > 127

    h, w = mask.shape

    visited = np.zeros_like(mask, bool)
    output = np.zeros_like(mask, bool)

    ys, xs = np.where(mask)

    for y0, x0 in zip(ys, xs):

        if visited[y0, x0]:
            continue

        stack = [(int(y0), int(x0))]
        visited[y0, x0] = True
        component = []

        while stack:

            y, x = stack.pop()
            component.append((y, x))

            neighbours = [
                (y - 1, x),
                (y + 1, x),
                (y, x - 1),
                (y, x + 1)
            ]

            for ny, nx in neighbours:

                if (
                    0 <= ny < h
                    and 0 <= nx < w
                    and mask[ny, nx]
                    and not visited[ny, nx]
                ):
                    visited[ny, nx] = True
                    stack.append((ny, nx))

        if len(component) >= min_size:

            for y, x in component:
                output[y, x] = True

    return output


# =========================================================
# VEGETATION
# =========================================================

def vegetation_score(image):
    a = arr(image)

    r = a[:, :, 0]
    g = a[:, :, 1]

    return (g - r) / (g + r + 1)


# =========================================================
# WATER
# =========================================================

def water_score(image):
    a = arr(image)

    r = a[:, :, 0]
    g = a[:, :, 1]
    b = a[:, :, 2]

    return (
        (g + b - 2 * r)
        /
        (g + b + 2 * r + 1)
    )


# =========================================================
# BUILT-UP
# =========================================================

def builtup_score(image):
    a = arr(image)

    r = a[:, :, 0]
    g = a[:, :, 1]
    b = a[:, :, 2]

    brightness = (
        r + g + b
    ) / (3 * 255.0)

    vegetation = (
        g - r
    ) / (g + r + 1)

    maximum = np.maximum.reduce([r, g, b])
    minimum = np.minimum.reduce([r, g, b])

    saturation = (
        maximum - minimum
    ) / (maximum + 1)

    return (
        0.55 * brightness
        - 0.30 * np.clip(
            vegetation,
            -1,
            1
        )
        - 0.15 * saturation
    )


# =========================================================
# FEATURE CHANGE
# =========================================================

def feature_change(
    before_score,
    after_score,
    mode
):

    difference = after_score - before_score

    if mode == "increase":
        raw = difference

    elif mode == "decrease":
        raw = -difference

    else:
        raw = np.abs(difference)

    threshold = adaptive_threshold(
        np.abs(raw),
        93,
        0.07
    )

    mask = clean_mask(
        raw > threshold,
        max(
            20,
            raw.size // 20000
        )
    )

    return mask, threshold


# =========================================================
# CONSTRUCTION CHANGE
# =========================================================

def construction_change(before, after):

    before_smooth = Image.fromarray(
        np.clip(
            smooth(before),
            0,
            255
        ).astype(np.uint8)
    )

    after_smooth = Image.fromarray(
        np.clip(
            smooth(after),
            0,
            255
        ).astype(np.uint8)
    )

    before_score = builtup_score(
        before_smooth
    )

    after_score = builtup_score(
        after_smooth
    )

    increase = (
        after_score - before_score
    )

    after_cutoff = float(
        np.percentile(
            after_score,
            60
        )
    )

    change_cutoff = adaptive_threshold(
        np.maximum(
            increase,
            0
        ),
        94,
        0.055
    )

    mask = (
        (increase > change_cutoff)
        &
        (after_score > after_cutoff)
    )

    mask = clean_mask(
        mask,
        max(
            30,
            mask.size // 25000
        )
    )

    return mask, change_cutoff


# =========================================================
# GENERAL CHANGE
# =========================================================

def general_change(before, after):

    before_smooth = smooth(before)
    after_smooth = smooth(after)

    score = np.mean(
        np.abs(
            after_smooth - before_smooth
        ) / 255.0,
        axis=2
    )

    threshold = adaptive_threshold(
        score,
        94,
        0.12
    )

    mask = clean_mask(
        score > threshold,
        max(
            20,
            score.size // 25000
        )
    )

    return mask, threshold


# =========================================================
# MAIN ANALYSIS FUNCTION
# =========================================================

def run_analysis(before, after, intent):

    if intent == "vegetation_increase":

        mask, threshold = feature_change(
            vegetation_score(before),
            vegetation_score(after),
            "increase"
        )

        color = [0, 220, 80]

        name = "🌳 Vegetation Increase Map"

        explanation = (
            "Green regions are candidate areas "
            "where the RGB vegetation signal increased. "
            "This prototype is not a true NDVI calculation."
        )

    elif intent == "vegetation_decrease":

        mask, threshold = feature_change(
            vegetation_score(before),
            vegetation_score(after),
            "decrease"
        )

        color = [255, 170, 0]

        name = "🍂 Vegetation Decrease Map"

        explanation = (
            "Orange regions are candidate areas "
            "where the RGB vegetation signal decreased."
        )

    elif intent == "water_change":

        mask, threshold = feature_change(
            water_score(before),
            water_score(after),
            "change"
        )

        color = [0, 150, 255]

        name = "💧 Water-body Change Map"

        explanation = (
            "Blue regions indicate candidate "
            "water-related changes using an RGB "
            "water proxy."
        )

    elif intent == "water_decrease":

        difference = (
            water_score(after)
            -
            water_score(before)
        )

        threshold = adaptive_threshold(
            np.abs(difference),
            93,
            0.07
        )

        mask = clean_mask(
            difference < -threshold,
            max(
                20,
                difference.size // 25000
            )
        )

        color = [0, 120, 255]

        name = "💧 Water Reduction Map"

        explanation = (
            "Blue regions indicate candidate "
            "areas where the RGB water signal decreased."
        )

    elif intent == "construction_increase":

        mask, threshold = construction_change(
            before,
            after
        )

        color = [255, 50, 50]

        name = "🏗️ Built-up Change Map"

        explanation = (
            "Red regions are candidate new "
            "built-up/construction areas."
        )

    else:

        mask, threshold = general_change(
            before,
            after
        )

        color = [255, 0, 0]

        name = "🔄 General Change Map"

        explanation = (
            "Red regions show the strongest "
            "smoothed RGB differences using "
            "an adaptive threshold."
        )

    changed = int(mask.sum())

    total = mask.size

    percentage = (
        changed / total * 100
    )

    return {
        "mask": mask,
        "threshold": threshold,
        "color": color,
        "name": name,
        "explanation": explanation,
        "changed": changed,
        "total": total,
        "pct": percentage,
        "intent": intent
    }


# =========================================================
# CREATE OVERLAY
# =========================================================

def create_overlay(image, mask, color):

    result = (
        arr(image) * 0.78
    ).astype(np.uint8)

    result[mask] = np.asarray(
        color,
        dtype=np.uint8
    )

    return result


# =========================================================
# CHANGE LEVEL
# =========================================================

def get_change_level(percentage):

    if percentage < 2:
        return "Low"

    if percentage < 8:
        return "Moderate"

    if percentage < 20:
        return "High"

    return "Very High"