# Air Force 11

<table>
  <tr>
    <td>Why ?</td>
     <td>Because.</td>
  </tr>
  <tr>
    <td><img src="img/Question.png" ></td>
    <td><img src="img/Air_Force_1.png" ></td>
  </tr>
 </table>


## Setup python project

First clone the project

```bash
git clone git@github.com:berradiayounes/air-force-11.git
```

We're using the python native environment manager for our development workflow. 
For more info, click [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

To setup the environment and the dependencies:

```bash
python3 -m venv air-force-11
python3 -m pip install -r requirements.txt
```

## Command Line Instructions (CLI)

### Activate the pipenv environment

```bash
source air-force-11/bin/activate
```

### Command Lines

* **Main command** 

```bash
python main.py
```

* **Options**

    ```bash
    python main.py --from_scratch 
    ```
   Create the preprocessed dataframe and run the rest with the default options

    ```bash
    python main.py --method nmf
    ```
    Use NMF to create embeddings and generate topics

    ```bash 
    python main.py --method gensim
    ```
    Use LDA to generate topics


## Linting

We use [black](https://github.com/psf/black) as our default linter.

 