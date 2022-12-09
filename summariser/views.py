from rest_framework import status, generics, parsers
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import Audio
from .serializers import AudioInputSerializer, SummaryOutputSerializer
from django.conf import settings
import ffmpeg
import speech_recognition as sr
import os

class GenerateSummary(generics.GenericAPIView):
    serializer_class = AudioInputSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    @swagger_auto_schema(operation_description="Summary Generation (Transcript)",
                         responses={ 201: 'Generated Successfully',
                                400: 'Given audio is of invalid format'})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # try:
            audio = Audio(audio=data['audio'], num_speakers=data['num_speakers'])
            audio.save()

            diarization = settings.PIPELINE(audio.audio.path)
            diarize_results = list()
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
                diarize_results.append([speaker, round(turn.start, 1), round(turn.end, 1)])
            
            
            r = sr.Recognizer()
            audio_input = ffmpeg.input(audio.audio.path)

            name = os.path.basename(audio.audio.name)

            
            for i, d in enumerate(diarize_results):
                audio_cut = audio_input.audio.filter('atrim', start=d[1], end=d[2])
                audio_output = ffmpeg.output(audio_cut, f'audios/cuts/{name}_cut{i+1}.wav')
                ffmpeg.run(audio_output)

            transcript = list()

            for i, d in enumerate(diarize_results):

                with sr.AudioFile(f'audios/cuts/{name}_cut{i+1}.wav') as source:
                    # r.adjust_for_ambient_noise(source)
                    aud = r.record(source)
                
                try:
                    transcript.append(f"{d[0]}: {r.recognize_google(aud)}")
                except:
                    transcript.append(f"{d[0]}: ERROR OCCURRED !!!!")

            transcript = '\n'.join(transcript)
            audio.transcript = transcript
            audio.save()
            return Response({'Success': "Summary Generated Successfully", 'transcript': transcript}, status=status.HTTP_201_CREATED)
            # except Exception as e:
            #     return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


