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

import requests

from openai import api_request

# OpenAI API key
API_KEY = os.environ.get('OPENAI_API_KEY')
if not API_KEY:
    print("OPENAI_API_KEY envvar required, quitting.")
    sys.exit(1)

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
  out: "
"""

def get_shell_command(dictation: str) -> str:
    prompt = prompt_template.replace('{dictation}', dictation)
    print(f"prompt:\n{prompt}")
    response = api_request(
        API_ENDPOINT,
        API_PARAMS,
        API_HEADERS,
        prompt,
    )
    command = response['choices'][0]['text']
    print(f"command:\n{command}")
    return command

def main():
    print('---')
    dictation = input('next dictation:\n')
    cmd = get_shell_command(dictation)
    if not input('enter any text to abort: '):
        os.system(cmd)

if __name__ == '__main__':
    while 1:
        main()
