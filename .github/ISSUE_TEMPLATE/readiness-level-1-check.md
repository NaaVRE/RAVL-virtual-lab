---
name: Readiness level 1 check
about: Issue to check the recommendations for readiness level 1.
title: Readiness level 1 check
labels: ''
assignees: ''

---

The following has been implemented in the virtual lab:
* Documentation
  - [ ] The virtual lab metadata is available outside the virtual lab.
    - [ ] Metadata is tracked by version control.
* Security
  - [ ] Personal tokens are not tracked by version control.
* Versioning
  - [ ] Versions of used software and libraries are pinned.
* Data
  - [ ] The data is ready for scientific experiments.
  - [ ] Data that is only read by the virtual lab is stored in an external catalogue.
* Codebase
  - [ ] The code executes without errors: The code can be executed without errors.
Currently, you can verify this by manually executing all cells in the notebook on a machine on which the code was not developed (to ensure no references are made to local resources).
  - [ ] The responsibility of each cell in the notebook is clear and can be described in a single sentence.
  - [ ] The coding style is consistent and follows a style guide e.g. For Python [PEP 8](https://peps.python.org/pep-0008/).
  - [ ] Parallel processing is applied where suitable.
  - [ ] There are clear errors when expected files and objects are not found.
  - [ ] External code use, such as command-line interface tools, are clearly labeled.
* Containerization
  - [ ] The notebook cells can be containerized.
* Workflow execution
  - [ ] The containerized cells can run without any modifications.
  - [ ] It is possible to give a demonstration of the virtual lab.
