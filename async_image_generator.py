"""
Author: Emil Mirzayev

This script generates images based on prompts for different country groups using the DeepInfra API.
It allows for customization of image parameters and provides cost estimation before execution.

Features:
- Asynchronous image generation for improved performance
- Configurable number of images per country group
- Customizable image dimensions and inference steps
- Option to resize generated images
- Cost estimation and user confirmation before execution
- Saves generated images in separate folders for each country group

Usage:
python async_image_generator.py [--n_per_country N] [--width W] [--height H] 
                                [--num_inference_steps S] [--model MODEL] [--resize]

Requirements:
- Python 3.7+
- Required packages: aiohttp, Pillow, python-dotenv
- DeepInfra API key (set in .env file)
- config.json file with country groups, prompts, and other configuration details

Note: Ensure you have sufficient API credits before running large batches.
"""

import aiohttp
import asyncio
import json
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os
import random
import argparse
import sys

# Load the .env file from the current directory
load_dotenv()

DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')

async def generate_image(session, api_key, prompt, width, height, num_inference_steps, model):
    if model == "schnell":
        url = "https://api.deepinfra.com/v1/inference/black-forest-labs/FLUX-1-schnell"
    elif model == "dev":
        url ="https://api.deepinfra.com/v1/inference/black-forest-labs/FLUX-1-dev"
    else:
        return None
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {"prompt": prompt, "width": width, "height": height, "num_inference_steps": num_inference_steps}
    json_data = json.dumps(data)

    async with session.post(url, headers=headers, data=json_data) as response:
        if response.status == 200:
            response_data = await response.json()
            image_data = response_data['images'][0].split(',')[1]
            image_bytes = base64.b64decode(image_data)
            return image_bytes
        else:
            return None

def save_image(image_bytes, folder, filename, resize=False):
    if image_bytes:
        os.makedirs(folder, exist_ok=True)
        full_path = os.path.join(folder, filename)
        
        # Open the image using PIL
        image = Image.open(BytesIO(image_bytes))
        
        # Resize the image if the resize option is True
        if resize:
            image = image.resize((256, 256), Image.LANCZOS)
        
        # Save the image
        image.save(full_path)
        print(f"Image saved as {full_path}")
    else:
        print("Failed to generate or save the image.")

def get_next_image_number(folder):
    os.makedirs(folder, exist_ok=True)
    existing_files = [f for f in os.listdir(folder) if f.endswith('.png')]
    return len(existing_files) + 1


def calculate_total_images(config, n_per_country):
    return len(config['countries']) * n_per_country

def ask_user_confirmation(total_images, total_cost):
    print(f"\nPotential cost of this run: ${total_cost:.4f} for {total_images} images")
    while True:
        response = input("Do you want to proceed? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please answer with 'yes' or 'no'.")

def calculate_cost(width, height, num_inference_steps):
    return 0.0005 * (width / 1024) * (height / 1024) * num_inference_steps

async def generate_images_for_country_group(session, country_group, config, n_per_country, width, height, num_inference_steps, model, resize):
    print(f"\nGenerating images for {country_group}")
    folder_name = f"generated_images/{country_group}"
    os.makedirs(folder_name, exist_ok=True)

    tasks = []
    for i in range(n_per_country):
        country = random.choice(config['countries'][country_group])
        facial_characteristics = random.choice(config['facial_characteristics'])
        hair = random.choice(config['hair'])

        prompt = config['prompt'].format(
            country=country,
            facial_characteristics=facial_characteristics if facial_characteristics else "no facial hair",
            hair=hair
        )

        print(f"Generated prompt: {prompt}")

        task = asyncio.create_task(generate_image(
            session=session,
            api_key=DEEPINFRA_API_KEY,
            prompt=prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            model=model
        ))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
            if image_bytes:
                next_number = get_next_image_number(folder_name)
                file_name = f"{country_group}{next_number}.png"
                save_image(image_bytes, folder_name, file_name, resize)


    return len([img for img in image_bytes_list if img is not None])

async def main():
    parser = argparse.ArgumentParser(description="Generate images for country groups")
    parser.add_argument("--n_per_country", type=int, default=1, help="Number of images to generate per country group. Defaults to 1")
    parser.add_argument("--width", type=int, default=512, help="Width of the generated images. Defaults to 512")
    parser.add_argument("--height", type=int, default=512, help="Height of the generated images. Defaults to 512")
    parser.add_argument("--num_inference_steps", type=int, default=1, help="Number of inference steps. Defaults to 1")
    parser.add_argument("--model", type= str, default= "schnell", help= "The model to be used. Must be one of `schnell` or `dev`. Schnell is cheaper and faster")
    parser.add_argument("--resize", action="store_true", help="Resize images to 256x256 if set")

    args = parser.parse_args()

    with open('config.json', 'r') as f:
        config = json.load(f)

    total_images = calculate_total_images(config, args.n_per_country)
    total_cost = total_images * calculate_cost(args.width, args.height, args.num_inference_steps)

    if not ask_user_confirmation(total_images, total_cost):
        print("Operation cancelled by user.")
        sys.exit(0)

    generated_images = 0
    async with aiohttp.ClientSession() as session:
        tasks = []
        for country_group in config['countries'].keys():
            task = asyncio.create_task(generate_images_for_country_group(
                session, country_group, config, args.n_per_country,
                args.width, args.height, args.num_inference_steps,
                args.model, args.resize
            ))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        generated_images = sum(results)

    actual_cost = generated_images * calculate_cost(args.width, args.height, args.num_inference_steps)

    print("\nImage generation complete for all country groups.")
    print(f"Total images generated: {generated_images}")
    print(f"Actual cost of this run: ${actual_cost:.4f}")

if __name__ == "__main__":
    asyncio.run(main())

