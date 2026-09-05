pipeline {
    agent { label 'docker-vm' }

    stages {
        stage('Run Playwright Tests') {
            steps {
                withCredentials([string(credentialsId: 'DOQA_TOKEN', variable: 'DOQA_TOKEN')]) {
                    sh '''
                        echo "🚀 Запускаем Playwright-контейнер..."
                        docker run --rm --ipc=host \
                            -v ${WORKSPACE}:/app \
                            -e DOQA_TOKEN=${DOQA_TOKEN} \
                            -e DOQA_SPACE_ID=${DOQA_SPACE_ID} \
                            my-playwright:latest \
                            pytest . --cache-clear -v --maxfail=5
                    '''
                }
            }
        }
    }

    post {
        always {
            sh '''
                echo "📦 Генерируем Allure-отчёт для Jenkins..."
                cd /home/ubuntu/jenkins/workspace/playwright-test
                if [ -d "allure-results" ]; then
                    allure generate allure-results -c -o allure-report
                else
                    echo "⚠️ Папка allure-results не найдена"
                fi
            '''

            allure results: [[path: 'allure-report']]
        }
    }
}