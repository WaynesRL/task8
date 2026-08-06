pipeline {
    agent any

    parameters {
        choice(
            name: 'STEP',
            choices: ['checkout', 'delete', 'push'],
            description: 'checkout = Job_1, delete = Job_2, push = Job_3'
        )
    }

    environment {
        REPO_URL        = 'git@172.19.0.2:8929/task8/task8.git'
        BRANCH          = 'main'
        REPO_DIR        = '/var/jenkins_home'   // локальное хранилище
        FILES_TO_DELETE = 'Task1.py Task2.py'
        GIT_USER        = 'Jenkins'
        GIT_EMAIL       = 'project_1_bot_414d9e3bc7bb069b2fad0c832431f0d3@noreply.gitlab-server'
    }

    options {
        skipDefaultCheckout(true)
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timestamps()
    }

    stages {

        /* ================= Job_1: код из master в локальное хранилище ================= */
        stage('Job_1: clone/pull master') {
            when { expression { params.STEP == 'checkout' } }
            steps {
                sshagent(credentials: ["${CRED_ID}"]) {
                    sh '''
                        set -e
                        if [ ! -d "$REPO_DIR/.git" ]; then
                            git clone "$REPO_URL" "$REPO_DIR"
                        fi
                        cd "$REPO_DIR"
                        git config user.name  "$GIT_USER"
                        git config user.email "$GIT_EMAIL"
                        git fetch origin
                        git checkout "$BRANCH"
                        git reset --hard "origin/$BRANCH"
                        git clean -fd
                        echo "=== HEAD ==="; git log -1 --oneline
                        echo "=== Files ==="; ls -1
                    '''
                }
                // защита от рекурсии: если последний коммит сделал сам Jenkins — стоп
                script {
                    def msg = sh(script: "cd $REPO_DIR && git log -1 --pretty=%s",  returnStdout: true).trim()
                    def ae  = sh(script: "cd $REPO_DIR && git log -1 --pretty=%ae", returnStdout: true).trim()
                    if (msg.contains('[ci skip]') || ae == env.GIT_EMAIL) {
                        currentBuild.description = 'Свой коммит — цепочка не запускается'
                        env.CHAIN = 'stop'
                    }
                }
            }
            post {
                success {
                    script {
                        if (env.CHAIN != 'stop') {
                            build job: 'Job_2', wait: false,
                                  parameters: [string(name: 'STEP', value: 'delete')]
                        }
                    }
                }
            }
        }

        /* ================= Job_2: удалить 1-2 файла ================= */
        stage('Job_2: delete files') {
            when { expression { params.STEP == 'delete' } }
            steps {
                sh '''
                    set -e
                    cd "$REPO_DIR"
                    for f in $FILES_TO_DELETE; do
                        if [ -f "$f" ]; then
                            git rm -f "$f"; echo "Удалён: $f"
                        else
                            echo "Нет файла (пропуск): $f"
                        fi
                    done
                    git status --short
                '''
            }
            post {
                success {
                    build job: 'Job_3', wait: false,
                          parameters: [string(name: 'STEP', value: 'push')]
                }
            }
        }

        /* ================= Job_3: вернуть проект в Git ================= */
        stage('Job_3: commit & push') {
            when { expression { params.STEP == 'push' } }
            steps {
                sshagent(credentials: ["${CRED_ID}"]) {
                    sh '''
                        set -e
                        cd "$REPO_DIR"
                        if git diff --cached --quiet; then
                            echo "Изменений нет — push не требуется."; exit 0
                        fi
                        git commit -m "Jenkins Job_3: удаление файлов (build #${BUILD_NUMBER}) [ci skip]"
                        git push origin "HEAD:$BRANCH"
                        echo "Запушено в $BRANCH."
                    '''
                }
            }
        }
    }

    post {
        failure { echo "Шаг ${params.STEP} упал — см. Console Output." }
    }
}
