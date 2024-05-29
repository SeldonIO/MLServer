# Contributing to MLServer

Opening a PR
------------
* Fork the repository from `SeldonIO` into local Github account. 
* create a branch from the master of the forked repository.<br> `git checkout -b <branch>`.
<br> branches can be named as `bug|feat|doc|`_`<desc>`_`<optional params>`
* make changes, and raise a PR from local repository `<branch>` to main repository `master`.
* make sure that your branch is always uptodate (you may use rebase to resolve conflicts) with **SeldonIO/MLServer** `master` branch. <br>
```bash
   git remote add upstream https://github.com/SeldonIO/MLServer.git 
   git fetch upstream
   git checkout <your_branch_name>
   git rebase upstream/master
```

Installation for Contributing
------------
- git clone the forked repository: <br>`git clone <your-repo>/MLServer <your-folder>` 
- setup `mlserver`: ```pip install .```
- run examples in debugging mode and verify execution taking one to breakpoints in one's development branch

Raising a PR
------------
- Choose a default PR template/templates available underneath `/docs/PULL_REQUEST_TEMPLATE/` as a `template` query param. 

_Before opening a pull request_ consider:

- Is the change important and ready enough to ask the community to spend time reviewing?
- Have you searched for existing, related issues and pull requests?
- Is the change being proposed clearly explained and motivated?

When you contribute code, you affirm that the contribution is your original work and that you
license the work to the project under the project's open source license. Whether or not you
state this explicitly, by submitting any copyrighted material via pull request, email, or
other means you agree to license the material under the project's open source license and
warrant that you have the legal authority to do so.
