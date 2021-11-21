# Advent of Code 2020

My solutions to Advent of Code 2020

## Usage

I use conda for this project, so some of my code (mostly, the `init_day.sh` stuff) assumes you do the same.

You can initialize a new day by running `./init_day.sh` from the project root directory. It will attempt to activate a
conda environment before running `helpers/init_day.py`.

You can set defaults for this script by creating a copy of `.env.example` and renaming to `.env`. Then, set the values
inside to customize the init script!
