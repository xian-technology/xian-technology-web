import asyncio

import reflex as rx


class ToolingState(rx.State):
    """UI state local to the tooling page."""

    sdk_install_copied: bool = False

    async def copy_sdk_install_command(self):
        """Copy the SDK install command and flash copy feedback."""
        self.sdk_install_copied = True
        yield rx.set_clipboard("uv add xian-tech-py")
        await asyncio.sleep(1.4)
        self.sdk_install_copied = False


__all__ = ["ToolingState"]
