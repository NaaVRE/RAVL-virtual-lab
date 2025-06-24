---
name: Readiness level 2 check
about: Issue to check the recommendations for readiness level 2.
title: Readiness level 2 check
labels: ''
assignees: ''

---

The following has been implemented in the virtual lab:
* User community
  - [ ] Other potential users have been identified.
* Data
  - [ ] All input data of the lab is FAIR.
* Metadata
  - [ ] All the fields of the metadata standard are present.
* Scenarios
  - [ ] The virtual lab can be used in multiple scenarios, i.e. both the parameters and datasets can be changed to suit experiments of different researchers.
* Documentation
  - [ ] There is a [user manual](../user_manual) and at least one domain scientist who was not involved in the development of the virtual lab has reviewed the user manual.
The coding experience of the reviewer of the user manual is similar to the coding experience of the intended user.
  - [ ] How to use the virtual lab on a different scenario is explained.
* Codebase
  - [ ]  Unit tests verify the behavior of used methods and libraries. There should be a testing guideline, which will be done in this issue [\#274](https://github.com/QCDIS/projects_overview/issues/274).
  - [ ]  The virtual lab reads, writes and exchanges data in a way that meets domain-relevant community standards. Recommendations for what standards to use are under investigation, see github issue [#281](https://github.com/QCDIS/projects_overview/issues/281).
  - [ ]  The code within cells is easily human-readable and others can easily modify it. If methods have side effects, this is clear to the user.
  - [ ]  The input and output of each cell is clear. It is both clear what the structure is (e.g. what data type is used) and what the data content is from a domain perspective.
* Workflow
  - [ ]  The duration of computation, memory usage, and power usage of the containers is acceptable. As there is currently no dashboard to monitor resource usage, contact the VLIC team for guidelines.
* Deployment
  - [ ] The virtual lab is publicly available.
* Infrastructure
  - [ ]  The infrastructure requirements for the workshop are known and the necessary infrastructure has been provided:
    - [ ]  The number of people taking part in a workshop.
    - [ ]  The random access memory and permanent storage usage of the virtual lab are known.
    - [ ]  The amount of processors the virtual lab uses is known.
