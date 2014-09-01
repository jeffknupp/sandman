# How to contribute

For `sandman` to be a truly great project, third-party code contributions are
critical. I (@jeffknupp) can only do so much, and I don't have the benefit of
working on `sandman` in a team, where multiple ideas and points-of-view would be
heard. So if you want to enhance `sandman`, spot and fix a bug, or just
generally want to get involved, I'd love the help! Below is a list of things
that might aid you in contributing to `sandman`.

## Getting Started

* Create a new, Python 2.7+ virtualenv and install the requirements via pip: `pip install -r requirements.txt`
* Make sure you have a [GitHub account](https://github.com/signup/free)
* Either submit an issue directly on GitHub or head to `sandman's` [Waffle.io](https://waffle.io/jeffknupp/sandman) page
  * For bugs, clearly describe the issue including steps to reproduce
  * For enhancement proposals, be sure to indicate if you're willing to work on implementing the enhancement
* Fork the repository on GitHub

## Making Changes

* `sandman` uses [git-flow](http://nvie.com/posts/a-successful-git-branching-model/) as the git branching model
    * **No commits should be made directly to `master`**
    * [Install git-flow](https://github.com/nvie/gitflow) and create a `feature` branch like so: `$ git flow feature start <name of your feature>`
* Make commits of logical units.
* Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure you have added the necessary tests for your changes.
    * Test coverage is currently at 100% and tracked via [coveralls.io](https://coveralls.io/r/jeffknupp/sandman?branch=develop)
    * Aim for 100% coverage on your code
        * If this is not possible, explain why in your commit message
        * This may be an indication that your code should be refactored
    * If you're creating a totally new feature, create a new class in `test_sandmand.py` that inherits from `TestSandmanBase`
* Run `python setup.py test` to make sure your tests pass
* Run `coverage run --source=sandman setup.py test` if you have the `coverage` package installed to generate coverage data
* Check your coverage by running `coverage report`

## Submitting Changes

* Push your changes to the feature branch in your fork of the repository.
* Submit a pull request to the main repository

# Additional Resources

* [Issue tracker (Waffle.io)](https://waffle.io/jeffknupp/sandman)
* [General GitHub documentation](http://help.github.com/)
* [GitHub pull request documentation](http://help.github.com/send-pull-requests/)
