# ChatBot for Running Route Planning

This chatbot is designed to interact with users and gather information about their desired running routes. Using Natural Language Processing (NLP), the chatbot fills specific slots to understand user preferences and generate appropriate responses.

---

## Features

- Conversational interface to determine running route preferences.
- Slot-filling mechanism to capture key details:
  - **Difficulty**
  - **Route length**
  - **Start location**
  - **Start number**
  - **End location**
  - **Location end number**
  - **Location start number**
- Architecture based on modular design:
  1. **NLU + Rule-based**: Creates BIO tags for user input.
  2. **Tracker**: Fills and tracks slots based on BIO-tagged input.
  3. **Policy**: Determines the chatbot's next response.
  4. **NLG**: Generates responses using deep learning.

---

## Installation

Follow these steps to set up and run the chatbot:

### Prerequisites

Ensure you have Python installed (>=3.7).

### Install Requirements

Install the required dependencies:

```bash
pip install -r req.txt
```

Download the SpaCy model:

```bash
python -m spacy download en_core_web_sm
```

---

## Usage

### Download Required Folder

Before running the chatbot, download the required folder from the following link:
[Download Folder](https://drive.google.com/drive/folders/1m6Iu3DjrN0Ybvo4hMyYgX1RtPtiads6Z?usp=sharing)

Extract the folder and note its directory path.

### Run the Chatbot

Run the chatbot using:

```bash
python main.py <path_to_downloaded_folder>
```

Replace `<path_to_downloaded_folder>` with the directory path of the folder you downloaded.

Interact with the chatbot to plan your running route. It will guide you by asking questions and filling the required slots.

---

## Screenshots

_Add screenshots of the chatbot in action here._

---

## File Structure

- **main.py**: Main script to run the chatbot.
- **nlu_model.py**: Handles BIO tagging for user input.
- **tracker.py**: Tracks and fills slots.
- **policy.py**: Determines chatbot responses.
- **nlg_model.py**: Generates responses.
- **req.txt**: Dependencies file.
- **All_trials**: A folder containing the progress we made in order to build the bot

---

## How It Works

1. **NLU + Rule-based Model**:

   - Processes user input.
   - Tags input using BIO tagging.

2. **Tracker**:

   - Tracks filled slots.
   - Ensures all required slots are completed.

3. **Policy**:

   - Decides the next action of the chatbot (e.g., ask a question or finalize the route).

4. **NLG**:
   - Generates natural responses using a deep learning model.

---

## Contribution

Feel free to contribute by submitting issues or pull requests to enhance the chatbot! 😎

---
