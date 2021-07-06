0.3.33 (2021-07-06)
-------------------

- Allow to define the container name
  [bloodbare]


0.3.32 (2021-07-01)
-------------------

- Add exceptions in case there is conflict or not found
  [bloodbare]


0.3.31 (2021-05-12)
-------------------

- Added suport to set template metadata annotations
  [sunbit]


0.3.30 (2021-05-11)
-------------------

- Fix typo in previous release
  [sunbit]


0.3.29 (2021-05-11)
-------------------

- Fix typo in previous release
  [sunbit]


0.3.28 (2021-05-11)
-------------------

- Added support to set a job containers as privileged
  [sunbit]


0.3.27 (2020-11-11)
-------------------

- Adding nodeSelector
  [bloodbare]


0.3.26 (2020-08-24)
-------------------

- Nothing changed yet.


0.3.25 (2020-08-24)
-------------------

- Adding affinity and toleration
  [bloodbare]


0.3.24 (2020-08-21)
-------------------

- Adding deployment logic
  [bloodbare]


0.3.23 (2019-10-07)
-------------------

- Adding imagePullPolicy parameter on jobs
  [bloodbare]


0.3.22 (2019-09-29)
-------------------

- Adding labels on job and fixing tests
  [bloodbare]


0.3.21 (2019-07-25)
-------------------

- Adding image pull secrets
  [bloodbare]


0.3.20 (2019-07-24)
-------------------

- Support of base64 ca and fixing bugs
  [bloodbare]


0.3.19 (2018-06-10)
-------------------

- bump


0.3.18 (2018-06-05)
-------------------

- Provide keywords on jobs
  [ramonnb]


0.3.17 (2018-06-04)
-------------------

- Provide more defaults for nomad jobs
  [vangheem]


0.3.16 (2018-06-04)
-------------------

- Provide purge option on deletion for k8s and nomad
  [ramonnb]


0.3.15 (2018-06-04)
-------------------

- Error using nomad list of args
  [vangheem]


0.3.14 (2018-05-23)
-------------------

- Missed file scale.py
  [ramonnb]


0.3.13 (2018-05-23)
-------------------

- Adding support to scale up and down nomad jobs
  [ramonnb]


0.3.12 (2018-05-22)
-------------------

- Removing a warning
  [ramonnb]


0.3.11 (2018-05-21)
-------------------

- Adding support to scale up and down deployments
  [ramonnb]


0.3.10 (2018-05-05)
-------------------

- Be able to specific kubernetes API and use non-ssl endpoints
  [vangheem]

0.3.9 (2018-04-27)
------------------

- Adding support to delete executions
  [ramonnb]

- Adding testing support for in-cluster tests
  [ramonnb]

0.3.8 (2018-04-18)
------------------

- Handle no `env` value for k8s `Job.get_payload`
  [vangheem]


0.3.7 (2018-04-17)
------------------

- Make sure restart policy is set to never
  [vangheem]


0.3.6 (2018-04-17)
------------------

- Build fixes
  [vangheem]


0.3.5 (2018-04-17)
------------------

- Provide error message from k8s in exception
  [vangheem]


0.3.4 (2018-04-12)
------------------

- Add `get_config_maps` method to Manager
  [vangheem]


0.3.3 (2018-03-21)
------------------

- Load payload as json


0.3.2 (2018-03-20)
------------------

- bump.


0.3.1 (2018-03-20)
------------------

- Fix Nomad job implementation
  [vangheem]

0.3.0 (2018-03-19)
------------------

- initial release
