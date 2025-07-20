import asyncio
from audio_player import generate_audio

transcript = "Please mind the platform gap. <chinese>请注意月台空隙。 <malay>Sila berhati-hati ruang di platform. <tamil>தயவுசெய்து நடைமேடை இடைவெளியைக் கவனியுங்கள்."
asyncio.run(generate_audio(transcript))
print("Terminating script.")
