# Finance Tracker

## About the project

### Creating a receipt information extraction model

The steps for building the machine learning model are performed within the directory `receipt_ml`.

#### Preparing the data

1. First, images of receipts were acquired from online datasets.
   The sources are linked in a text file titled `img_sources.txt`.
   The following are some assumptions:
   - All images are JPEG files.
   - They have unique names.
   - They are located in a folder called `receipt_ml/image_dataset`.

Next, a ground truth dataset corresponding to each image was created.
To create the ground truth, the API for [GPT-4o](https://openai.com/api/) by OpenAI was used.

2. Prepare the data for use with the Batch API.
   To begin, run `gpt_json.py` inside the `data_preparation` directory.

   The script uses the prompt given in `gpt_prompt.txt` and the image dataset to wrap the data in JSONL files as required by Batch API.
   The task files generated are located in `data_preparation/batches`.
   Note that due to restrictions on API usage, multiple small task files are created, and hence, multiple Batch API requests are needed.
