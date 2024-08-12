import os
import json
import time
import google.generativeai as genai
from PIL import Image
from tqdm import tqdm
from pathlib import Path


def main(api_key:str, lower:int, upper:int, src:list, text_prompt:str):

    # suppress warnings
    os.environ["GRPC_VERBOSITY"] = "ERROR"
    os.environ["GLOG_minloglevel"] = "2"

    # use the api key
    genai.configure(api_key=api_key)

    # use gemini 1.5 flash
    model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"response_mime_type": "application/json"})

    # initialize lists
    results = []
    errors = []

    # grab responses from gemini
    for i in tqdm(range(lower, upper)):
        img_path = images_path[i]

        # open the image
        img = Image.open(img_path)

        # generate the model response json
        response = model.generate_content([img, llm_instructions])

        # try reading the model reponse json
        try:
            ans = json.loads(response.candidates[0].content.parts[0].text)
        except Exception as error:
            errors.append({"file": str(img_path), "error": str(error), "response": str(response)})
        
        # add succesful results
        results.append({"file": str(img_path), "response": ans})

        # sleep for 5 seconds due to api limits
        time.sleep(5)

    # write results to jsonl
    with open("results.jsonl", mode="a") as results_file:
        for img_response in results:
            results_file.write(json.dumps(img_response) + "\n")

    # write errors to jsonl
    with open("errors.jsonl", mode="a") as error_file:
        for img_error in errors:
            error_file.write(json.dumps(img_error) + "\n")

    return None


if __name__ == "__main__":
    # get API key from shell session
    # in shell, run
    # export API_KEY="YOUR API KEY"
    # (with the quotations!)
    api_key = os.environ["API_KEY"]

    # due to limits on API usage,
    # define the range of the images to be passed
    lower = 1400
    upper = 2800

    # list of image paths
    images_path = [x for x in Path("image_dataset").rglob("*.jpg")]

    # get the prompt
    with open("llm_prompt.txt", mode="r") as prompt_file:
        llm_instructions = "".join([x for x in prompt_file])

    main(api_key, lower, upper, images_path, llm_instructions)
