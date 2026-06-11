import unittest

from textual.widgets import OptionList

from app.ui.application import StackBaseApp


class TestStackBaseApplication(unittest.IsolatedAsyncioTestCase):
    async def test_application_starts_with_main_menu(self) -> None:
        application = StackBaseApp()

        async with application.run_test(size=(120, 40)):
            menu = application.query_one("#main-menu", OptionList)

            self.assertIsNotNone(menu)
            self.assertTrue(menu.has_focus)

    async def test_application_has_seven_menu_options(self) -> None:
        application = StackBaseApp()

        async with application.run_test(size=(120, 40)):
            menu = application.query_one("#main-menu", OptionList)

            self.assertEqual(menu.option_count, 7)

    async def test_q_closes_application(self) -> None:
        application = StackBaseApp()

        async with application.run_test(size=(120, 40)) as pilot:
            await pilot.press("q")

        self.assertFalse(application.is_running)


if __name__ == "__main__":
    unittest.main()
