from import_export import resources, fields
from .models import CarModel, CarBrand
from import_export.widgets import ForeignKeyWidget

class CarModelResource(resources.ModelResource):
    brand = fields.Field(
        column_name='Car Make',
        attribute='brand',
        widget=ForeignKeyWidget(CarBrand, 'name'))
    name = fields.Field(
        column_name='Model',
        attribute='name')
    internal_name = fields.Field(
        column_name='Model Internal Name',
        attribute='internal_name')
    production_start = fields.Field(
        column_name='production_start',
        attribute='production_start')
    production_end = fields.Field(
        column_name='production_end',
        attribute='production_end')


    class Meta:
        model = CarModel
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ["internal_name",]
        #fields = ('id', 'brand', 'name', 'internal_name', 'production_start', 'production_end')

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        start_lst = []
        end_lst = []
        brands = set()
        for row in dataset:
            start, end = map(int, row[3].split(" - "))
            start_lst.append(start)
            end_lst.append(end)
            brands.add(row[0])
        dataset.insert_col(3, col=start_lst, header="production_start")
        dataset.insert_col(4, col=end_lst, header="production_end")
        del dataset["Years of Production"]
        for brand_name in brands:
            CarBrand.objects.get_or_create(name=brand_name)