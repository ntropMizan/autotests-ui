pipeline {
    agent { label 'docker-vm' }

    stages {
        stage('Run Playwright Tests') {
            steps {
                sh '''
                    echo "🚀 Запускаем Playwright-контейнер..."
                    docker run --rm --ipc=host \
                        -v ${WORKSPACE}:/app \
                        -e DOQA_URL=https://o7g195.doqa.app \
                        -e DOQA_TOKEN=43d1faef-c620-43b6-9078-db9de7f76311 \
                        -e DOQA_SPACE_ID=2 \
                        my-playwright:latest \
                        pytest . --cache-clear -v --maxfail=5 --doqa
                '''
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