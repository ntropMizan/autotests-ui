import pytest
import allure
from playwright.sync_api import Page, expect

from pages.courses_list_page import CoursesListPage
from pages.create_course_page import CreateCoursePage


@allure.epic("Courses")
@allure.feature("Create Course")
@allure.story("Create new course")
@allure.title("Создание нового курса")
@allure.id(15)
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.courses
@pytest.mark.regression
def test_create_course(courses_list_page: CoursesListPage, create_course_page: CreateCoursePage):
    with allure.step("Открыть страницу создания курса"):
        create_course_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses/create")

    with allure.step("Проверить элементы формы создания курса"):
        create_course_page.check_visible_create_course_title()
        create_course_page.check_disabled_create_course_button()
        create_course_page.check_visible_image_preview_empty_view()
        create_course_page.check_visible_image_upload_view(is_image_uploaded=False)
        create_course_page.check_visible_create_course_form(
            title="", max_score="0", min_score="0", description="", estimated_time=""
        )

    with allure.step("Проверить секцию упражнений"):
        create_course_page.check_visible_exercises_title()
        create_course_page.check_visible_create_exercise_button()
        create_course_page.check_visible_exercises_empty_view()

    with allure.step("Загрузить изображение"):
        create_course_page.upload_preview_image("./testdata/files/image.png")
        create_course_page.check_visible_image_upload_view(is_image_uploaded=True)

    with allure.step("Заполнить форму создания курса"):
        create_course_page.fill_create_course_form(
            title="Playwright",
            max_score="100",
            min_score="10",
            description="Playwright",
            estimated_time="2 weeks"
        )
        create_course_page.click_create_course_button()

    with allure.step("Проверить, что курс создался"):
        courses_list_page.check_visible_courses_title()
        courses_list_page.check_visible_create_course_button()
        courses_list_page.check_visible_course_card(
            index=0, title="Playwright", max_score="100", min_score="10", estimated_time="2 weeks"
        )


@allure.epic("Courses")
@allure.feature("Course List")
@allure.story("Empty course list")
@allure.title("Просмотр пустого списка курсов")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.courses
@pytest.mark.regression
def test_empty_courses_list(chromium_page_with_state: Page):
    with allure.step("Открыть страницу со списком курсов"):
        chromium_page_with_state.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")

    with allure.step("Проверить заголовок Courses"):
        courses_title = chromium_page_with_state.get_by_test_id('courses-list-toolbar-title-text')
        expect(courses_title).to_be_visible()
        expect(courses_title).to_have_text('Courses')

    with allure.step("Проверить иконку пустого списка"):
        empty_view_icon = chromium_page_with_state.get_by_test_id('courses-list-empty-view-icon')
        expect(empty_view_icon).to_be_visible()

    with allure.step("Проверить заголовок пустого списка"):
        empty_view_title = chromium_page_with_state.get_by_test_id('courses-list-empty-view-title-text')
        expect(empty_view_title).to_be_visible()
        expect(empty_view_title).to_have_text('There is no results')

    with allure.step("Проверить описание пустого списка"):
        empty_view_description = chromium_page_with_state.get_by_test_id('courses-list-empty-view-description-text')
        expect(empty_view_description).to_be_visible()
        expect(empty_view_description).to_have_text('Results from the load test pipeline will be displayed here')