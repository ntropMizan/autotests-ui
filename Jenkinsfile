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
                            pytest . --alluredir=allure-results -v
                    '''
                }
            }
        }
    }

    post {
        always {
            withCredentials([string(credentialsId: 'DOQA_TOKEN', variable: 'DOQA_TOKEN')]) {
                sh '''
                    echo "📦 Подготавливаем Allure-результаты для DoQA..."
                    cd /home/ubuntu/jenkins/workspace/playwright-test

                    # Удаляем лишние файлы
                    rm -f allure-results/testrun.json || true
                    rm -f allure-results/executor.json || true
                    rm -rf allure-results/history || true

                    # Упаковываем только содержимое
                    cd allure-results
                    zip -r ../allure-results.zip .
                    cd ..

                    echo "🚀 Отправляем отчет в DoQA через API..."
                    curl -X POST https://o7g195.doqa.app/api/autotests/report \
                        -F "token=${DOQA_TOKEN}" \
                        -F "spaceId=${DOQA_SPACE_ID}" \
                        -F "file=@allure-results.zip" \
                        -F "type=allure" || echo "⚠️ Ошибка отправки"

                    echo "📦 Генерируем Allure-отчёт для Jenkins..."
                    if [ -d "allure-results" ]; then
                        allure generate allure-results -c -o allure-report
                    else
                        echo "⚠️ Папка allure-results не найдена"
                    fi
                '''
            }

            allure results: [[path: 'allure-report']]
        }
    }
}