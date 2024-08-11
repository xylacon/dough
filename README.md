# Finance Tracker

## About the project

### Creating a receipt information extraction model

The steps for building the machine learning model were performed within the directory `receipt_ml`.

#### Preparing the data

1. First, images of receipts were acquired from online datasets.
   The sources are linked in a text file titled `img_sources.txt`.
   The following are some assumptions:
   - All images are JPEG files.
   - They have unique names.
   - They are located in a folder called `receipt_ml/data_preparation/image_dataset`.

2. Next, a ground truth dataset corresponding to each image was created.
   To create the ground truth, the API for [Gemini 1.5 Flash](https://ai.google.dev/gemini-api) by Google was used.

   Run `ground_truth.py` inside the `data_preparation` directory.
   The script reads the prompt given in `llm_prompt.txt` and the image dataset, sends it to Gemini for a response.
   The responses are stored in `results.jsonl`, and errors in parsing the response to an image are recorded in `errors.jsonl`.

   **Note**

   Due to API usage limits, a lower and upper bound for the images sent is given.
   Depending on the size of the image dataset, the script was run over several days because of these restrictions.
   Be sure to change the bounds on each run.

3. Assume the results from the Batch API are stored as `JSONL` files inside `data_preparation/gpt_results`. -->
   <!-- To extract the results, run `gpt_extract.py`.

   Since GPT-4o-mini can make mistakes, a file of all -->
