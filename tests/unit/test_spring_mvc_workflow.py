import tempfile
import unittest
from pathlib import Path

from app.workflow.spring_mvc_workflow import SpringMvcWorkflow


class TestSpringMvcWorkflow(unittest.TestCase):
    def test_plans_and_applies_mvc_actions_only_after_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root_path = Path(temporary_directory)
            source_path = root_path / "src/main/java/com/example/demo"
            source_path.mkdir(parents=True)
            (root_path / "pom.xml").write_text(
                """
                <project>
                    <dependencies>
                        <dependency>
                            <groupId>org.springframework.boot</groupId>
                            <artifactId>spring-boot-starter-web</artifactId>
                        </dependency>
                    </dependencies>
                </project>
                """,
                encoding="utf-8",
            )
            (source_path / "DemoApplication.java").write_text(
                """
                package com.example.demo;

                import org.springframework.boot.autoconfigure.SpringBootApplication;

                @SpringBootApplication
                public class DemoApplication {
                }
                """,
                encoding="utf-8",
            )

            workflow = SpringMvcWorkflow()
            plan = workflow.plan(root_path)

            self.assertTrue(plan.can_apply)
            self.assertEqual(plan.package_name, "com.example.demo")
            self.assertTrue(
                any(
                    action.relative_path.as_posix().endswith("controller")
                    for action in plan.actions
                )
            )

            first_action = plan.actions[0]
            workflow.apply_action(root_path, first_action)

            self.assertTrue((root_path / first_action.relative_path).exists())
            self.assertFalse((root_path / "src/main/java/com/example/demo/service").exists())

    def test_rejects_non_spring_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root_path = Path(temporary_directory)
            workflow = SpringMvcWorkflow()
            plan = workflow.plan(root_path)

            self.assertFalse(plan.can_apply)
            self.assertFalse(plan.is_spring_boot_project)
            self.assertTrue(plan.warnings)


if __name__ == "__main__":
    unittest.main()
