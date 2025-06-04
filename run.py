# from watchfiles import awatch
# import subprocess
# import asyncio
#
#
# async def watch_and_reload():
#     print("Starting server...")
#     process = subprocess.Popen(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])
#
#     async for changes in awatch("app"):
#         print("Changes detected:", changes)
#         print("Restarting server...")
#         process.terminate()
#         process.wait()
#         process = subprocess.Popen(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])
#
# if __name__ == "__main__":
#     asyncio.run(watch_and_reload())


from watchfiles import awatch
import subprocess
import asyncio
import cProfile
import pstats
import tempfile
import os


async def watch_and_reload():
    print("Starting server...")
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # корень проекта
    PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # корень проекта

    env = os.environ.copy()
    env["PYTHONPATH"] = PROJECT_ROOT

    process = subprocess.Popen(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],cwd=CURRENT_DIR)

    async for changes in awatch(CURRENT_DIR):
        print("Changes detected:", changes)
        print("Restarting server...")
        process.terminate()
        process.wait()
        process = subprocess.Popen(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],cwd=CURRENT_DIR)


async def profile_target():
    await watch_and_reload()


def main():
    # Создаём временное место для сохранения профиля
    profile_file = os.path.join(tempfile.gettempdir(), "watch_reload_profile.prof")
    print(f"Profiling to {profile_file}")

    # Запускаем с профилированием
    profiler = cProfile.Profile()
    profiler.enable()

    try:
        asyncio.run(profile_target())
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        profiler.disable()
        profiler.dump_stats(profile_file)

        # Выводим статистику в консоль
        stats = pstats.Stats(profiler)
        stats.sort_stats(pstats.SortKey.TIME).print_stats(20)

        print(f"Profile saved to {profile_file}")
        #snakeviz "C:\Users\SAVOST~1.VA\AppData\Local\Temp\watch_reload_profile.prof"


if __name__ == "__main__":
    main()

