# Register for an API KEY at https://platform.openai.com/overview
#
# Write a function that takes Mac dictation as input and returns a shell command.
# Uses OpenAI's python module to translate the dictation result.
#
# Example:
#   $ python3 dictation_to_shell.py
#   > "CD…"
#   $ cd ..
#
#   $ python3 dictation_to_shell.py
#   > "LSA"
#   $ ls -a
#
#   $ python3 dictation_to_shell.py
#   > "CD to the Desktop"
#   $ cd ~/Desktop
#
#   $ python3 dictation_to_shell.py
#   > "move food at pie to Bardock pie"
#   $ mv foo.py bar.py

import os
import sys
import subprocess

import openai


# OpenAI API key
API_KEY = os.environ.get('OPENAI_API_KEY')
if not API_KEY:
    print("OPENAI_API_KEY envvar required, quitting.")
    sys.exit(1)
openai.api_key = API_KEY

# OpenAI API endpoint
API_ENDPOINT = 'https://api.openai.com/v1/engines/davinci/completions'

# OpenAI API parameters
API_PARAMS = {
    'max_tokens': 50,
    'temperature': 0.7,
    'top_p': 0.9,
    'n': 1,
    'stream': True,
    'logprobs': None,
    'stop': '\n',
}

# OpenAI API headers
API_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + API_KEY,
}


PROMPT = """
Bash, Mac
Examples:
  in: "LSA"
  out: ls -a

  in: "CD to the Desktop"
  out: cd ~/Desktop

  in: "move food at pie to Bardock pie"
  out: mv foo.py bar.py

  in: "{dictation}"
"""

def get_shell_command(dictation: str) -> str:
    prompt = PROMPT.replace('{dictation}', dictation)
    # print(f"prompt:\n{prompt}")
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        top_p=0.9,
        n=5,
        stop="\n",
    )
    choices = []
    for resp in response["choices"]:
        ch = resp['text'].strip()
        if ch.startswith('out: '):
            ch = ch[5:]
            choices.append(ch)
    for i, ch in enumerate(choices):
        print(f'choice {i}:\n\t{ch}')
    choice = input("Which command? Press enter to abort. : ")
    if choice:
        choice = int(choice)
        command = choices[choice]
        print(f"command:\n{command}")
        return command

def repl():
    print('---')
    dictation = input('next dictation:\n')
    cmd = get_shell_command(dictation)
    if cmd:
        exit_code, output = subprocess.getstatusoutput(cmd)
        if exit_code:
            print(f'nonzero exit code: {exit_code}')
        if output:
            print(output)

def main():
    while 1:
        repl()

if __name__ == '__main__':
    main()
