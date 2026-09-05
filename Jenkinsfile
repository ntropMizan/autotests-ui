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
                    echo "📦 Подготавливаем Allure-результаты..."
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

        stage('Allure Report Server') {
            steps {
                sh '''
                    echo "🌐 Запускаем Allure-сервер для локального просмотра..."
                    cd /home/ubuntu/jenkins/workspace/playwright-test

                    # Останавливаем предыдущий сервер
                    pkill -f "allure open" || true

                    # Запускаем Allure-сервер на порту 8081
                    nohup allure open allure-results --port 8081 > /tmp/allure-server.log 2>&1 &

                    echo "✅ Allure-сервер запущен на http://192.168.252.2:8081"
                    echo "📋 Логи: cat /tmp/allure-server.log"
                '''
            }
        }
    }

    post {
        always {
            allure results: [[path: 'allure-results']]
        }
    }
}