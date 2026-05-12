# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

Convert photographs of mathematical knots into Regina code for computational knot theory (polynomial invariants, etc.). The pipeline: image → detect crossings → classify each crossing (type + angle) → emit Regina code.

## Session Start Reminder

Always remind the user to activate the virtual environment at the start of every session. Tell the user with a chill message like: "Hey, don't forget to activate the environment! The command is: `.\venv\Scripts\activate`"

## Running the Code

All active development is in Jupyter notebooks — `Main.py` is a skeletal placeholder. Run notebooks from the `scripts/` directory so relative paths resolve correctly.

```bash
# Generate/regenerate synthetic training data (outputs to data/local_Knot_training_data/)
jupyter notebook scripts/Training_Data_Creator.ipynb

# Train the model / run the interactive DrawerApp tester
jupyter notebook scripts/Neural_Network.ipynb

# Image processing experiments and contour detection on real knot photos
jupyter notebook scripts/Test-Funtions.ipynb
```

## Architecture

### Pipeline stages

1. **Training_Data_Creator.ipynb** — generates 8,000 synthetic 64×64 crossing images with JSON labels (`labels.json`, `labels_train.json`, `labels_val.json`). Each image is one crossing patch with a random angle and one of 5 crossing types.

2. **Neural_Network.ipynb** — defines, trains, and interactively tests `DualHeadKnotNet`. Also contains `KnotDataset` and all channel-building helpers. The trained model is saved to `data/local_Knot_training_data/best_model.pth`.

3. **Test-Funtions.ipynb** — applies CV (contour detection, etc.) to real knot photos to extract crossing patches for inference.

4. **Main.py** — intended entry point with a `Link` class; not yet functional.

### DualHeadKnotNet

4-channel 64×64 input tensor built by helpers shared across notebooks:
- **Ch1**: grayscale, normalized to `[-1, 1]`
- **Ch2**: direction dot drawn at radius 22 px from center (encodes traversal angle spatially)
- **Ch3/4**: Sobel X/Y gradients, scaled ×5

Shared conv backbone (4→32→64→128 channels, three MaxPool stages) → 8192 features, then two independent heads:
- **Angle head** → `[cos θ, sin θ]`; angle recovered at inference via `atan2`. Loss: cosine distance, **masked** for `empty` and `full` classes where angle is undefined.
- **Crossing head** → 5-class logits. Loss: CrossEntropy.

Combined loss: `0.5 * angle_loss + 0.5 * crossing_loss`.

### Crossing classes

| Index | Name |
|-------|------|
| 0 | overcrossing |
| 1 | undercrossing |
| 2 | line |
| 3 | empty |
| 4 | full |

`empty` and `full` have no meaningful angle — the angle loss mask excludes indices ≥ 3.

### Key constants (defined in both notebooks — keep in sync)

```python
WINDOW_SIZE = (64, 64)
DOT_RADIUS_FROM_CENTER = 22
DOT_DRAW_RADIUS = 3
CROSSING_TO_IDX = {"overcrossing":0, "undercrossing":1, "line":2, "empty":3, "full":4}
```

### Channel helpers

`make_dot_channel()` and the Sobel helpers are duplicated in both `Training_Data_Creator.ipynb` and `Neural_Network.ipynb`. Any change to these must be applied in both places.
