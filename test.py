import pika
from models import Contact
from mongoengine import connect
from faker import Faker

fake = Faker()

def create_fake_contacts(n):
    contacts = []
    for _ in range(n):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            additional_info=fake.text()
        )
        contact.save()
        contacts.append(contact)
    return contacts

def send_to_queue(contact_ids):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    for contact_id in contact_ids:
        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=str(contact_id))
    connection.close()

def main():
    connect('email_db')  # Підключення до бази даних MongoDB
    contacts = create_fake_contacts(10)  # Генерація 10 фейкових контактів
    send_to_queue([contact.id for contact in contacts])

if __name__ == "__main__":
    main()
    print(f"test")
    print(f"test2")