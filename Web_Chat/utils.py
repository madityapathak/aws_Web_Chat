from django.db.models import Count,Max,Q


def remove_duplicates_from_table(model, lookup_fields):
    duplicates = (
        model.objects.values(*lookup_fields)
        .order_by()
        .annotate(min_id=Max('id'), count_id=Count('id'))
        .filter(count_id__gt=1)
    )

    fields_lookup = Q()
    duplicate_fields_values = duplicates.values(*lookup_fields)
    for val in duplicate_fields_values:
        fields_lookup |= Q(**val)
    min_ids_list = duplicates.values_list('min_id', flat=True)

    if fields_lookup:
        model.objects.filter(fields_lookup).exclude(id__in=min_ids_list).delete()




# the motive of this function is to remove andy duplicate entries from database of any model
# however it is not yet used in any part of program it was usef in notifications model 
# but i removed it form that task as i found another way for this purpose 