from rest_framework.response import Response
class DataMixin:
    def get(self, request):


        skip = int(request.GET.get('skip', 0))
        limit = int(request.GET.get('limit', -1))
        objs = self.model.objects.all()

        if skip >= len(objs):
            return Response(
                {
                    'status':'skipped value greater than amount of objects',
                    'posts': self.serializer_class([], many=True).data
                },
                status=400,
            )
        objs = objs[skip:]

        if limit < -1:
            return Response(
                {
                    'status': 'limit less than 0',
                    'posts': self.serializer_class([], many=True).data
                },
                status=400,
            )
        if limit != -1:
            objs = objs[:limit]
        return Response({'posts': self.serializer_class(objs, many=True).data})

    def post(self, request):
        id = int(request.data.get('id', -1))
        model = self.model()
        try:
            model = self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            pass

        serializer = self.serializer_class(model, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({'post': serializer.data})