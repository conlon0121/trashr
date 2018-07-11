from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=10, default='')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Email(models.Model):
    email = models.EmailField()
    receives_alerts = models.BooleanField(default=True)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class Dumpster(models.Model):
    # Utility flags
    TRASH = 0
    RECYCLING = 1
    COMPOST = 2
    org = models.ForeignKey(Organization, default=1, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    rfid = models.CharField(max_length=50, default='')
    capacity = models.IntegerField(default=0)
    capacity_units = models.CharField(max_length=20, default='')
    container_type = models.CharField(max_length=50, default='')
    coordinates = ArrayField(
        models.DecimalField(max_digits=12, decimal_places=8)
    )
    core_id = models.CharField(max_length=25, default='')
    # Whether or not the sensor is sending readings
    functioning = models.BooleanField(default=True)
    utility = models.PositiveSmallIntegerField(default=0)
    percent_fill = models.SmallIntegerField(default=0)
    alert_percentage = models.SmallIntegerField(default=70)
    last_updated = models.DateTimeField(null=True, blank=True)
    alert_sent = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.address)
    
    @property
    def get_utility(self):
        return {
                '0': 'Trash',
                '1': 'Recycling',
                '2': 'Compost'
                }[str(self.utility)]


class IntervalReading(models.Model):
    raw_readings = ArrayField(models.SmallIntegerField(default=0))
    dumpster = models.ForeignKey(Dumpster, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp) + ' ' + str(self.dumpster)


class Pickup(models.Model):
    dumpster = models.ForeignKey(Dumpster, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Alert(models.Model):
    fill_percent = models.PositiveSmallIntegerField(default=70)
    timestamp = models.DateTimeField(auto_now_add=True)
    dumpster = models.ForeignKey(Dumpster, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.timestamp)


class PaymentMethod(models.Model):
    card_id = models.CharField(max_length=30, default="")
    customer_id = models.CharField(max_length=30, default="")
    card_type = models.CharField(max_length=20, default="")
    last_four_digits = models.CharField(max_length=20, default="")
    expires = models.DateField()
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.last_four_digits + ': ' + str(self.expires)


# Stripe needs a product for their subscription service
class Product(models.Model):
    id = models.CharField(max_length=30, default="", primary_key=True)
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


# Stripe needs a plan as well for their subscription service
class Plan(models.Model):
    id = models.CharField(max_length=30, default="", primary_key=True)
    name = models.CharField(max_length=50, default="")
    # Frequency with which to charge in months
    charge_frequency = models.IntegerField(default=1)
    # Amount to charge in pennies
    charge_amount = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    id = models.CharField(max_length=30, default="", primary_key=True)
    plan = models.ForeignKey(Plan, default=1)
    org = models.ForeignKey(Organization)
    charge_date = models.SmallIntegerField(default=25)
    start_date = models.DateTimeField(auto_now_add=True)
    sensor_count = models.SmallIntegerField(default=1)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)

    def __str__(self):
        return self.org.name


class Transaction(models.Model):
    amount = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)
    filled_datetime = models.DateTimeField(blank=True, null=True)
    subscription = models.ForeignKey(Subscription, related_name='transactions', null=True, blank=True)
    # Used if the subscription does not yet exist when the transactions come in.
    subscription_string = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.status + " " + str(self.created_datetime)
