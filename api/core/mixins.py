from rest_framework.exceptions import ValidationError
from rest_framework.response import Response




class DataMixin:




    def get(self, request):
        skip = int(request.GET.get('skip', 0))
        limit = int(request.GET.get('limit', -1))

        filters = {}

        for i in request.GET:
            if i not in ['skip', 'limit']:
                filters[i] = request.GET[i]


        objs = self.model.objects.filter(**filters)

        if skip >= len(objs):
            return Response(self.serializer_class(objs, many=True).data)
        objs = objs[skip:]

        if limit < -1:
            return Response(
                {
                    'error': 'limit less than 0',
                },
                status=400,
            )
        if limit != -1:
            objs = objs[:limit]
        return Response(self.serializer_class(objs, many=True).data)

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

