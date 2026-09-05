pipeline {
    agent { label 'docker-vm' }

    stages {
        stage('Run Playwright Tests') {
            steps {
                sh '''
                    echo "🚀 Запускаем Playwright-контейнер..."
                    cd /home/ubuntu/jenkins/workspace/playwright-test
                    docker run --rm --ipc=host -v $PWD:/app \
                        my-playwright:latest \
                        pytest --alluredir=/app/allure-results -v --maxfail=5
                '''
            }
        }

        stage('Prepare Allure Results') {
            steps {
                sh '''
                    echo "📦 Подготавливаем Allure-результаты для DoQA..."
                    cd /home/ubuntu/jenkins/workspace/playwright-test

                    sudo chown -R ubuntu:ubuntu allure-results/ || true
                    chmod -R 755 allure-results/ || true

                    cd allure-results
                    rm -f testrun.json executor.json
                    rm -rf history
                    zip -r ../allure-results.zip *-result.json *-container.json
                    cd ..
                '''
            }
        }
    }

    post {
        always {
            sh '''
                echo "📤 Отправляем отчет в DoQA..."
                cd /home/ubuntu/jenkins/workspace/playwright-test
                curl -X POST https://o7g195.doqa.app/api/autotests/report \
                    -F "token=43d1faef-c620-43b6-9078-db9de7f76311" \
                    -F "spaceId=2" \
                    -F "file=@allure-results.zip" \
                    -F "type=allure"
                echo "✅ Отчет отправлен в DoQA!"
            '''

            allure results: [[path: 'allure-results']]
        }
    }
}