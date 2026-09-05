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

        stage('Prepare and Send Allure Results') {
            steps {
                withCredentials([string(credentialsId: 'DOQA_TOKEN', variable: 'DOQA_TOKEN')]) {
                    sh '''
                        echo "📦 Подготавливаем и отправляем Allure-результаты..."
                        cd /home/ubuntu/jenkins/workspace/playwright-test

                        # Очистка от лишних файлов
                        rm -f allure-results/testrun.json || true
                        rm -f allure-results/executor.json || true
                        rm -rf allure-results/history || true

                        # Создание архива
                        cd allure-results
                        zip -r ../allure-results.zip .
                        cd ..

                        # Отправка отчета через официальную утилиту doqa
                        docker run --rm \
                            -v ${WORKSPACE}:/app \
                            my-playwright:latest \
                            doqa report https://o7g195.doqa.app/api/autotests/report \
                                ${DOQA_SPACE_ID} \
                                ${DOQA_TOKEN} \
                                /app/allure-results.zip \
                                allure
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
                fi
            '''
            allure results: [[path: 'allure-report']]
        }
    }
}