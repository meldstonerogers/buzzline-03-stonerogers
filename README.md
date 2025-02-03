# buzzline-03-stonerogers
Streaming Data, Project 3
Melissa Stone Rogers, [GitHub](https://github.com/meldstonerogers/buzzline-03-stonerogers)

## Introduction

This is a professional project using Apache Kafka to create uniquie JSON and CSV producers and consumers to simulate streaming data. Python Version 3.11 was used, as well as Git for version control. 
This project was forked from Dr. Case's project repository found [here](https://github.com/denisecase/buzzline-03-case). Much of the detailed instructions in this README.md were borrowed from Dr. Case's project specifications, and updated for my machine.
Commands were used on a Mac machine running zsh.   

Streaming data can be structured (e.g. csv files) or semi-structured (e.g. json data). 

We'll work with two different types of data, and so we'll use two different Kafka topic names. 
See [.env](.env). 


## Task 1. Use Tools from Previous Repo Specifications 

Before starting, ensure you have first completed the setup tasks in [Project 1](https://github.com/denisecase/buzzline-01-case) and [Project 2](https://github.com/denisecase/buzzline-02-case), created by Dr. Case. 
Python 3.11 is required. 

## Task 2. Copy This Example Project and Rename

Once the tools are installed, copy/fork this project into your GitHub account and create your own version of this project to run and experiment with.
Name it `buzzline-03-yourname` where yourname is something unique to you.
Follow the instructions in [FORK-THIS-REPO.md](https://github.com/denisecase/buzzline-01-case/blob/main/docs/FORK-THIS-REPO.md).
    

## Task 3. Manage Local Project Virtual Environment

Follow the instructions in [MANAGE-VENV.md](https://github.com/denisecase/buzzline-01-case/blob/main/docs/MANAGE-VENV.md) to:
1. Create your .venv
2. Activate .venv
3. Install the required dependencies using requirements.txt.

```zsh
python3.11 -m venv .venv
source .venv/bin/activate
```
```zsh
python -m pip install --upgrade pip setuptools wheel
python -m pip install --upgrade -r requirements.txt

```

Remember, each time a new terminal is opened, activate the .venv. 
```zsh
source .venv/bin/activate
```

### Initial Project Commit 
Turn on the autosave function in VS Code. Push changes to GitHub freqently to effectively track changes. Update the commit message to a meaningful note for your changes. 
```zsh
git add .
git commit -m "initial"                         
git push origin main
```

## Task 4. Start Zookeeper and Kafka (2 Terminals)

If Zookeeper and Kafka are not already running, you'll need to restart them.
See instructions at [SETUP-KAFKA.md] to:

1. Start Zookeeper Service ([link](https://github.com/denisecase/buzzline-02-case/blob/main/docs/SETUP-KAFKA.md#step-7-start-zookeeper-service-terminal-1))
2. Start Kafka ([link](https://github.com/denisecase/buzzline-02-case/blob/main/docs/SETUP-KAFKA.md#step-8-start-kafka-terminal-2))

## Task 5. Customize JSON Producer

Make customizations to the JSON Producer. I modified this code to use polars. I wanted to try using polars to read and handle the JSON data. I adjusted the generate_messages fucntion to utilize polars with the following: 
```zsh
def generate_messages(file_path: pathlib.Path):
    while True:
        try:
            logger.info(f"Opening data file: {DATA_FILE}")

            # Read JSON file into a Polars DataFrame
            df = pl.read_json(DATA_FILE)

            # Convert each row to a dictionary and yield
            for buzz_entry in df.to_dicts():
                logger.debug(f"Generated JSON: {buzz_entry}")
                yield buzz_entry

        except FileNotFoundError:
            logger.error(f"File not found: {file_path}. Exiting.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error processing JSON file with Polars: {e}")
            sys.exit(3)
```            

In VS Code, open a terminal. Use the commands below to activate .venv, and start the producer. 

```zsh
source .venv/bin/activate
python3 -m producers.json_producer_stonerogers
```

## Task 6. Customize JSON Consumer

Make customizations to the JSON Consumer. I modified in the following way: 

In VS Code, open a NEW terminal in your root project folder. Use the commands below to activate .venv, and start the consumer. 

```zsh
source .venv/bin/activate
python3 -m consumers.json_consumer_stonerogers
```

## Task 7. Customize CSV Producer

Make customizations to the CSV Producer. I modified in the following way: 

In VS Code, open a NEW terminal in your root project folder. Use the commands below to activate .venv, and start the producer. 

```zsh
source .venv/bin/activate
python3 -m producers.csv_producer_stonerogers
```

## Task 8. Customize a CSV Consumer

Make customizations to the CSV Consumer. I modified in the following way: 

In VS Code, open a NEW terminal in your root project folder. Use the commands below to activate .venv, and start the consumer. 

```zsh
source .venv/bin/activate
python3 -m consumers.csv_consumer_stonerogers
```

## About the Smart Smoker (CSV Example)

A food stall occurs when the internal temperature of food plateaus or 
stops rising during slow cooking, typically between 150°F and 170°F. 
This happens due to evaporative cooling as moisture escapes from the 
surface of the food. The plateau can last for hours, requiring 
adjustments like wrapping the food or raising the cooking temperature to 
overcome it. Cooking should continue until the food reaches the 
appropriate internal temperature for safe and proper doneness.

The producer simulates a smart food thermometer, sending a temperature 
reading every 15 seconds. The consumer monitors these messages and 
maintains a time window of the last 5 readings. 
If the temperature varies by less than 2 degrees, the consumer alerts 
the BBQ master that a stall has been detected. This time window helps 
capture recent trends while filtering out minor fluctuations.

## Later Work Sessions
When resuming work on this project:
1. Open the folder in VS Code. 
2. Start the Zookeeper service.
3. Start the Kafka service.
4. Activate your local project virtual environment (.env).

## Save Space
To save disk space, you can delete the .venv folder when not actively working on this project.
You can always recreate it, activate it, and reinstall the necessary packages later. 
Managing Python virtual environments is a valuable skill. 

## Complete Your Project
Save your project and push back to your repository. 
```zsh
git add .
git commit -m "final"                         
git push origin main
```

## License
This project is licensed under the MIT License as an example project. 
You are encouraged to fork, copy, explore, and modify the code as you like. 
See the [LICENSE](LICENSE.txt) file for more.
