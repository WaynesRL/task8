pipeline {
    agent any

    parameters {
        choice (name: STEP, choices: ['clone', 'delete', 'push'],
                description: 'clone = Job_1, delete = Job_2, push = Job_3')
    }

    environment {
        GITHUB_REPO         = 'github.com/WaynesRL/task8'
        BRANCH              = 'main'
        REPO_DIR            = '/var/jenkins_home/local'
        FILES_TO_DELETE     = 'Task1.py Task2.py'
        GIT_USER            = 'WaynesRL'
        GIT_EMAIL           = 'waynesdb@gmail.com'
        CRED_ID             = 'github-pat'
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    options {
        skipDefaultCheckout(true)
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {

        /* Job_1 */
        stage('Job_1: clone from main to local') {
            when { expression { params.STEP == 'clone' } }
            steps {
                withCredentials([usernamePassword(credentialsId: env.CRED_ID,
                    usernameVariable: 'GITHUB_LOGIN',
                    passwordVariable: 'GITHUB_TOKEN')]) {

                sh '''
                    set -e
                    URL="{GITHUB_REPO}"
                    if [ ! -d "$REPO_DIR/.git" ]; then
                        git clone "$URL" "$REPO_DIR"
                    fi
                    cd "$REPO_DIR"
                    git remote set-url origin "$URL"
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
            }
                    post {
                        success {
                            script {
                                    build job: 'Job_2', wait: false,
                                        parameters: [string(name: 'STEP', value: 'delete')]
                        }
                    }
                }
            }
    
    /* Job_2 */
    stage('Job_2: delete files') {
        when { expression {params.STEP == 'delete'} }
        steps {
            sh '''
                set -e
                cd "$REPO_DIR"
                for f in $FILES_TO_DELETE; do
                    if [ -f "$f" ]; then git rm -f "$f"; echo "Files deleted";
                    else echo "Files not found"
                    fi
                done
                git status
                '''
        }
        post {
            success {
                build job: 'Job_3', wait: false,
                        parameters: [string(name: 'STEP', value: 'push')]
            }
        }
    }

    /* Job_3 */
    stage('Job_3: push') {
        when { expression { params.STEP == 'push' } }
        steps {
            sh '''
                set -e
                cd "$REPO_DIR"
                if git diff --cached --quiet; then
                    echo "No diff"; exit 0
                fi
                git commit -m "Jenkins Job_3: (build #${BUILD_NUMBER}) [ci skip]"
                git push origin "HEAD:$BRANCH"
                echo "Pushed to $BRANCH"
                '''
        }

    post { failure { echo "echo: Step ${params.STEP} was failed" } }
        }
    }
}
