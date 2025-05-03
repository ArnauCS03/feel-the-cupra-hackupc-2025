from class_bot import GeminiLiveAssistant
import asyncio
import os
import glob

if __name__ == "__main__":
    assistant = GeminiLiveAssistant(
        system_instruction=(
            "You are a helpful assistant who only answers based on the CUPRA Tavascan 2024 owner's manual and it's very concise and don't add at the end if the user needs help."
            "If the question is outside the manual, say so clearly."
        )
    )

    async def run_examples():

        base_folder = os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(base_folder, "audio_outputs")
        os.makedirs(output_folder, exist_ok=True)

        while True:
            message = input("\nUser> ")
            if message.lower() == "exit":
                # Clean up all .wav files in the current folder
                current_folder = os.path.dirname(os.path.abspath(__file__))
                for wav_file in glob.glob(os.path.join(output_folder, "*.wav")):
                    try:
                        os.remove(wav_file)
                    except Exception as e:
                        print(f"⚠️ Failed to delete {wav_file}: {e}")
                print(f"\n 🗑️  All the .wav files are deleted")
                break
            
            # Unique response path
            response_path = os.path.join(output_folder, f"response_{hash(message) % 10000}.wav")

            # 1) text → audio playback
            wav_file = await assistant.chat_and_play(message, output_wav=response_path) 
    

            # 2) audio → text transcript
            transcript = await assistant.transcribe_audio(wav_file)
            print("Assistant>", transcript)

    asyncio.run(run_examples())
