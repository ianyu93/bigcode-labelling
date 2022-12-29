# Setup


First clone the repo and cd into it.
```
git clone git@github.com:ianyu93/bigcode-labelling.git
cd bigcode-labelling
```

Then install the label-studio package and run the setup script.
```
pip install label-studio
bash setup.sh tasks-fp /path/to/tasks.json code-fp /path/to/codes.json
```

Setup scripts does the following:
- Given a `tasks.json` and `codes.json`, it outputs a `pre_annotated_data.json` and `config.xml`. 
  - `tasks.json` is provided by labelling vendor, and `codes.json` is the original dataset.
  - `config.xml` is dynamically generated based on entities seen in the `codes.json` file.
- It then sets up a label-studio project with `config.xml` as the interface code.
- User has to input email and password, but these credentials are stored locally only. 
- Once logged in, select `bigcode-pii` project and import `pre_annotated_data.json`.

# Things I didn't get to:
Ideally, this would be Dockerized with dynamic inputs, but there were some bugs I didn't get to yet. Will be some future improvement if needed.



