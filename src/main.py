import asyncio

import uvloop


async def main() -> None:
    await asyncio.sleep(1)


if __name__ == "__main__":
    uvloop.run(main())
