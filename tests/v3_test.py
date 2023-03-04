import sys

import revChatGPT.V3 as gpt3
import argparse


def main():
    """
    Main function
    """
    print(
        """
    ChatGPT - Official ChatGPT API
    Repo: github.com/acheong08/ChatGPT
    """,
    )
    print("Type '!help' to show a full list of commands")
    print("Press Esc followed by Enter or Alt+Enter to send a message.\n")

    # Get API key from command line
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api_key",
        type=str,
        required=True,
        help="OpenAI API key",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.5,
        help="Temperature for response",
    )
    parser.add_argument(
        "--no_stream",
        action="store_true",
        help="Disable streaming",
    )
    parser.add_argument(
        "--base_prompt",
        type=str,
        default="You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
        help="Base prompt for chatbot",
    )
    parser.add_argument(
        "--proxy",
        type=str,
        default=None,
        help="Proxy address",
    )
    parser.add_argument(
        "--top_p",
        type=float,
        default=1,
        help="Top p for response",
    )
    parser.add_argument(
        "--reply_count",
        type=int,
        default=1,
        help="Number of replies for each prompt",
    )
    args = parser.parse_args()
    # Initialize chatbot
    chatbot = gpt3.Chatbot(
        api_key=args.api_key,
        system_prompt=args.base_prompt,
        proxy=args.proxy,
        temperature=args.temperature,
        top_p=args.top_p,
        reply_count=args.reply_count,
    )
    session = gpt3.create_session()
    completer = gpt3.create_completer(
        [
            "!help",
            "!exit",
            "!reset",
            "!rollback",
            "!config",
            "!engine",
            "!temperture",
            "!top_p",
            "!reply_count",
            "!save",
            "!load",
        ],
    )
    # Start chat
    while True:
        print()
        try:
            print("User: ")
            prompt = gpt3.get_input(session=session, completer=completer)
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit()
        if prompt.startswith("!") and chatbot.handle_commands(prompt):
            continue
        print()
        print("ChatGPT: ", flush=True)
        if args.no_stream:
            print(chatbot.ask(prompt, "user"))
        else:
            for response in chatbot.ask_stream(prompt):
                print(response, end="", flush=True)
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()
