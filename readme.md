# Football Manager AI Face Generator

## Overview

This tool generates AI faces for Football Manager, compatible with NewGan and similar AI face pack installers (FMRTE). It uses the DeepInfra API to create realistic player faces based on various ethnic groups and facial characteristics. The image generation model is Flux ('schnell' by default). You can obtain your DeepInfra API key from [here](https://deepinfra.com/).

Short tutorial on how to use: https://www.youtube.com/watch?v=vldujOEPWoo

## Requirements

- Python 3.7 or higher
- Football Manager (for playing)
- NewGan or compatible face pack installer (for installing it to Football Manager)
- DeepInfra API key

## Installation

1. Clone this repository or download the source files.
2. Install required Python packages:

`pip install -r requirements.txt`
3. Generate and replace your DeepInfra API key in the `.env` file.


## File Structure

- `async_image_generator.py`: Main script for generating images
- `config.json`: Configuration file for countries, facial characteristics, and prompts
- `remove_bg.py`: Script to remove backgrounds from generated images
- `.env`: File containing your DeepInfra API key

## Usage

### Generating Images

Run the main script with optional arguments:

`python async_image_generator.py [--n_per_country N] [--width W] [--height H] [--num_inference_steps S] [--model MODEL] [--resize]`

Arguments:
- `--n_per_country`: Number of images to generate per country group (default: 1)
- `--width`: Width of generated images (default: 512)
- `--height`: Height of generated images (default: 512)
- `--num_inference_steps`: Number of inference steps (default: 1)
- `--model`: Model to use, either "schnell" or "dev" (default: "schnell". "dev" is more EXPENSIVE)
- `--resize`: If set, resizes images to 256x256

Example:

`python async_image_generator.py --n_per_country 2 --width 1024 --height 1024 --num_inference_steps 2 --model dev --resize`

### Removing Backgrounds

After generating images, you can remove backgrounds using:

`python remove_bg.py [--directory DIR]`

Arguments:
- `--directory`: Path to the directory containing images (default: "generated_images")

## Configuration

Edit `config.json` to modify:
- Country groups and countries within each group. The faces will be based on the countries.
- Facial characteristics
- Hair styles
- The prompt template for image generation. I advise that you make minimal changes to the prompt.

## Output

Generated images are saved in the `generated_images` folder, organized by country group as it appears in any NewGan compatible facepack.

```
generated_images/
├── African/
├── Asian/
├── Caucasian/
├── Central European/
├── EECA/
├── Italmed/
├── MENA/
├── MESA/
├── SAMed/
├── Scandinavian/
├── Seasian/
├── South American/
├── SpanMed/
└── YugoGreek/
```

Some example outputs:

<img src="https://github.com/user-attachments/assets/e4d722db-f6eb-4de5-94e7-38eeacd4ed6e" alt="African2" width="250" height="250">
<img src="https://github.com/user-attachments/assets/179a8f3d-6ea4-4385-80e0-02a128dfff59" alt="African1" width="250" height="250">
<img src="https://github.com/user-attachments/assets/5c1005ff-fb63-4141-9827-756ce7f7146b" alt="South American2" width="250" height="250">
<img src="https://github.com/user-attachments/assets/5b4d3ad8-188c-490f-ba66-db87cf504b91" alt="South American1" width="250" height="250">
<img src="https://github.com/user-attachments/assets/e9cda4c3-0af6-4ff5-a5e0-dcab3209eee8" alt="SpanMed2" width="250" height="250">
<img src="https://github.com/user-attachments/assets/4f15bc80-891a-409b-bf5b-d33971b09bb7" alt="SpanMed1" width="250" height="250">
<img src="https://github.com/user-attachments/assets/9cb0d33a-351a-4643-8736-b79ff26b560d" alt="MESA2" width="250" height="250">



## Cost Calculation and User Confirmation

Before beginning the image generation process, the script calculates the potential total cost based on the DeepInfra API pricing and the number of images to be generated (details in this link: https://deepinfra.com/black-forest-labs/FLUX-1-schnell/). It then displays this information to the user and asks for confirmation before proceeding. This allows users to make an informed decision about the cost before committing to the image generation process.


## Troubleshooting

- Ensure your `.env` file is correctly set up with a valid API key.
- Check your internet connection if the script fails to connect to the API.
- Make sure you have sufficient credits in your DeepInfra account.

## Support

For issues or questions, please open an issue on the GitHub repository.

## License

This project is open-source and available under the MIT License.
