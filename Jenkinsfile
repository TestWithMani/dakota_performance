pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))
        timeout(time: 45, unit: 'MINUTES')
    }

    parameters {
        choice(
            name: 'TEST_SCOPE',
            choices: ['collect-only', 'smoke', 'marker', 'full'],
            description: 'collect-only is safe default for CI without credentials/UI dependencies.'
        )
        string(
            name: 'PYTEST_MARKER',
            defaultValue: 'reports',
            description: 'Used only when TEST_SCOPE=marker (examples: metro_areas, reports, custom_dashboards).'
        )
        booleanParam(
            name: 'RUN_ALLURE',
            defaultValue: true,
            description: 'Generate allure-results directory for report publishing.'
        )
        string(
            name: 'SF_CREDENTIALS_ID',
            defaultValue: 'sf-marketplace-creds',
            description: 'Jenkins Username/Password credentials ID for Salesforce login (required for smoke/marker/full).'
        )
    }

    environment {
        VENV_DIR = '.venv-jenkins'
        PYTEST_JUNIT = 'test-results/pytest.xml'
        ALLURE_DIR = 'allure-results'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv ${VENV_DIR}
                            . ${VENV_DIR}/bin/activate
                            python -m pip install --upgrade pip
                            pip install -r salesforce_tab_performance/requirements.txt
                        '''
                    } else {
                        bat '''
                            py -m venv %VENV_DIR%
                            call %VENV_DIR%\\Scripts\\activate
                            python -m pip install --upgrade pip
                            pip install -r salesforce_tab_performance/requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Static Validation') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            pytest -q --collect-only
                            pytest -q -m smoke --collect-only
                            pytest -q -m metro_areas --collect-only
                            pytest -q -m reports --collect-only
                            pytest -q -m custom_dashboards --collect-only
                        '''
                    } else {
                        bat '''
                            call %VENV_DIR%\\Scripts\\activate
                            pytest -q --collect-only
                            pytest -q -m smoke --collect-only
                            pytest -q -m metro_areas --collect-only
                            pytest -q -m reports --collect-only
                            pytest -q -m custom_dashboards --collect-only
                        '''
                    }
                }
            }
        }

        stage('Run UI Performance Tests') {
            when {
                expression { return params.TEST_SCOPE != 'collect-only' }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${params.SF_CREDENTIALS_ID}",
                    usernameVariable: 'SF_USERNAME',
                    passwordVariable: 'SF_PASSWORD'
                )]) {
                    script {
                        def allureArg = params.RUN_ALLURE ? "--alluredir=${env.ALLURE_DIR}" : ""
                        def pytestTarget = ''

                        if (params.TEST_SCOPE == 'smoke') {
                            pytestTarget = '-m smoke'
                        } else if (params.TEST_SCOPE == 'marker') {
                            pytestTarget = "-m ${params.PYTEST_MARKER}"
                        } else {
                            pytestTarget = ''
                        }

                        if (isUnix()) {
                            sh """
                                . ${VENV_DIR}/bin/activate
                                mkdir -p test-results
                                pytest -q ${pytestTarget} ${allureArg} --junitxml=${PYTEST_JUNIT}
                            """
                        } else {
                            bat """
                                call %VENV_DIR%\\Scripts\\activate
                                if not exist test-results mkdir test-results
                                pytest -q ${pytestTarget} ${allureArg} --junitxml=%PYTEST_JUNIT%
                            """
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if (fileExists('allure-results')) {
                    archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
                }
                if (fileExists('salesforce_tab_performance/performance_results.xlsx')) {
                    archiveArtifacts artifacts: 'salesforce_tab_performance/performance_results.xlsx', allowEmptyArchive: true
                }
                if (fileExists('test-results/pytest.xml')) {
                    junit testResults: 'test-results/pytest.xml', allowEmptyResults: true
                }
            }
        }
    }
}
