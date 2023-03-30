# node-manager
Web app for node manager 

# Requirements

FastAPI - [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

# Development

## Style Checking

Coding style is enforced using the [pre-commit](https://pre-commit.com/) package.

You can set up your local git repository so that these style checks are automatically triggered whenever you
make a new commit.

```shell
pip install pre-commit  # Install the pre-commit package
pre-commit install      # Install the pre-commit hooks defined in .pre-commit-config.yaml to the .git/ directory for this repo
```

Now whenever you make a commit, the style checks will run automatically and suggest changes to your code!
