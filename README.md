# compile-publication-list

Tired of manually creating a publication list for your CV or Website? This tool uses the NASA ADS system to automatically generate a publication list for you.

### Installation

No installation necessary. You need to have [the `ads` package](https://pypi.org/project/ads/) installed. Just clone this repository.

### Set up an ADS API token

This program requires an API token to use ADS. Here's how to obtain one:

1. Visit [NASA/ADS](https://ui.adsabs.harvard.edu/) to [sign up for an account](https://ui.adsabs.harvard.edu/user/account/register) if you don't have one.

2. Visit the [API Token page](https://ui.adsabs.harvard.edu/user/settings/token), log in with your ADS account and you will see an API token string. Copy that token string.

3. Set your token string to an environment variable named `ADS_API_TOKEN`. You can do that by running:
    ```bash
    # If you use bash or bash-like shells --
    export ADS_API_TOKEN="your token string here"
    ```
    ```csh
    # If you use csh or csh-like shells --
    setenv ADS_API_TOKEN "your token string here"
    ```
    You can put this line into your `~/.bashrc` or `~/.cshrc` file.

4. Alternatively, set your ADS token in the config file.

### Usage
1. Modify the config file for your specific needs.
2. Run python compile_latex.py default_config.ini (or the name of the config file you provided)

### TODOs:
Support for HTML will come in the future
   
