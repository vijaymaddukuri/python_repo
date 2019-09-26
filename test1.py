fetch:
   includes:
     activescale:
       revision: 5.4.1-ender-staging
       path: test-common
       git: git@gitlab.amplidata.com:product/activescale.git

variables:
  include!: "activescale/testdriver_common/variables.yaml:variables.*"

machine_templates:
  include!: "activescale/testdriver_common/machine_templates.yaml:machine_templates.*"

setup_templates:
  include!: "activescale/testdriver_common/setup_templates.yaml:setup_templates.*"

setups:
  default:
    backend: virtualbox2
    setup_template: 1s1b

provisioning:
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='push certificates']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='install single scalermarvin']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='install single backendmarvin']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='setup acl identities']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='generate s3cmd config for scaler']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='generate s3cmd config for backend']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='install single csg']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='configure single scaler']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='install dependencies']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='get marvin cli cfg']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='configure amplistor columns']"
  - include!: "activescale/testdriver_common/provision_steps.yaml:*[step='restart scalerd']"

testsuites:
  - name: ov-integration
    runner: nosetests
    test_host: local
    pip_args: --no-deps
    runner_args: tests/ov -sv --logging-level=INFO --tc-file cfg/environment.cfg --with-progressive
    test_output: test_results_ov.xml

log_collection:
  log_dir: logs
  logs:
    - include!: "activescale/testdriver_common/log_configs.yaml:*[name=scaler_default]"
    - include!: "activescale/testdriver_common/log_configs.yaml:*[name=backendng_default]"
    - include!: "activescale/testdriver_common/log_configs.yaml:*[name=crash_files]"
    - include!: "activescale/testdriver_common/log_configs.yaml:*[name=system_logs]"
    - include!: "activescale/testdriver_common/log_configs.yaml:*[name=marvin_config]"
    - include!: "activescale/testdriver_common/log_configs.yaml:*[name=testsuite_logs]"
    - name: flame_var
      machines:
       - "tag:scaler"
      paths:
       - subdir: flame_var
         path: /opt/ampli/var/run/sparkexecutor