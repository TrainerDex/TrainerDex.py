## Style
This is largely copied from Cog-Creators/Red-DiscordBot. I might change things eventually but this 'just works' for now.

Our style checker of choice, [black](https://github.com/ambv/black), actually happens to be an auto-formatter. The checking functionality simply detects whether or not it would try to reformat something in your code, should you run the formatter on it. For this reason, we recommend using this tool as a formatter, regardless of any disagreements you might have with the style it enforces.

Use the command `black --help` to see how to use this tool. The full style guide is explained in detail on [black's GitHub repository](https://github.com/ambv/black). **There is one exception to this**, however, which is that we set the line length to 99, instead of black's default 88. This is already set in `pyproject.toml` configuration file in the repo so you can simply format code with Black like so: `black <src>`.


## Environments
We will be using [poetry](https://github.com/python-poetry/poetry) to manage dependencies, once I start working on this again.


## Commit Messages
We are using [Semantic Commit Messages](https://seesparkbox.com/foundry/semantic_commit_messages).

```
feat: add hat wobble

^--^ ^------------^
| |
| +-> Summary in present tense.
|
+-------> Type: chore, docs, deps, feat, fix, refactor, style, or test.
```
