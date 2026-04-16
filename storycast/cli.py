from __future__ import annotations

import argparse

import uvicorn

from storycast.pipeline import StoryCastPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="StoryCast CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Run the full StoryCast pipeline")
    create.add_argument("--topic", required=True, help="Plain-English topic for the final short film")

    serve = subparsers.add_parser("serve", help="Start the StoryCast web app")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--reload", action="store_true")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "create":
        manifest = StoryCastPipeline().run(args.topic, progress_callback=lambda message: print(f"[storycast] {message}"))
        print(manifest.final_video_path)
        return

    if args.command == "serve":
        uvicorn.run("main:app", host=args.host, port=args.port, reload=args.reload)
        return

    parser.error("Unknown command")


if __name__ == "__main__":
    main()
