
# Mili Assistant

Mili is an advanced artificial assistant powered by the Meta Wit model and Google Bard. It possesses the ability to efficiently execute a wide range of user-assigned tasks. Moreover, Mili engages in human-like conversations, providing an immersive experience for users. This exceptional assistant is thoughtfully designed for utilization on the Windows platform.

Users can leverage Mili's versatile capabilities by requesting it to perform various tasks, such as playing songs, setting reminders, and translating user queries. Additionally, Mili offers entertainment features, allowing users to enjoy singing songs, engaging in riddles, sharing fun facts and poems, motivational quotes, and jokes. Moreover, Mili facilitates hands-free navigation by enabling users to open websites and applications through voice commands.


Furthermore, we have incorporated Mili's own mapping system, enabling users to effortlessly navigate to desired locations and conveniently access information about their current whereabouts. Moreover, Mili provides the functionality to inquire about weather forecasts and conveniently manage Wi-Fi and Bluetooth connectivity in a hands-free manner. Users can also rely on Mili for personalized movie recommendations and stay updated with the latest news by simply making a request.

Additionally, users have the capability to create and modify grocery lists, facilitating the efficient management of grocery items. Our system places utmost importance on security, providing users with a secure environment to store their confidential information. User secrets are stored using an advanced encryption algorithm, ensuring their privacy and protection. Furthermore, user passwords are securely stored using bcrypt hashing, adding an extra layer of security. Users can also exercise control over explicit content through the comprehensive settings offered by Mili, allowing for a personalized and safe experience.

## API Reference

#### Profanity Filter

```http
  https://neutrinoapi-bad-word-filter.p.rapidapi.com/bad-word-filter
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `content-type` | `string` | application/x-www-form-urlencoded |
| `X-RapidAPI-Key` | `string` | **Required**. Your API key |
| `X-RapidAPI-Host` | `string` | neutrinoapi-bad-word-filter.p.rapidapi.com |

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `content` | `string` |**Required**. Your query |
| `censor-character` | `string` | * |


#### Sentiment Analysis

```http
  https://api.api-ninjas.com/v1/sentiment?text={query}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `query`      | `string` | **Required**. Sentence whose sentiment is to be analyzed |
| `X-Api-Key` | `string` | **Required**. Your API key |


#### Enitity Recognition

```http
  https://microsoft-text-analytics1.p.rapidapi.com/entities/recognition/general
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `content-type` | `string` | application/json |
| `X-RapidAPI-Key` | `string` | **Required**. Your API key |
| `X-RapidAPI-Host` | `string` | microsoft-text-analytics1.p.rapidapi.com |

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `string` | 1 |
| `language` | `string` | en |
| `text` | `string` |**Required**. Your query |



#### Random Quotes

```http
  https://api.quotable.io/randomhttps://api.quotable.io/random
```

#### Random Facts

```http
  https://uselessfacts.jsph.pl/random.json?language=en
```


#### Trivia API

```http
  https://opentdb.com/api.php?amount=10&difficulty=medium&type=multiple
```

#### Weather Conditions

```http
  https://microsoft-text-analytics1.p.rapidapi.com/entities/recognition/general
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `X-RapidAPI-Key` | `string` | **Required**. Your API key |
| `X-RapidAPI-Host` | `string` |weatherapi-com.p.rapidapi.com |

| Headers | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `q` | `string` |**Required**. latitude, longitude |
| `days` | `string` | 3 |


#### Matrix API

```http
  https://trueway-directions2.p.rapidapi.com/FindDrivingRoute
```

| Headers | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `X-RapidAPI-Key` | `string` | **Required**. Your API key |
| `X-RapidAPI-Host` | `string` |trueway-directions2.p.rapidapi.com |

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| stops | `string` |**Required**. latitude, longitude |


## Features

- Translation into 107 different languages
- Play songs
- Navigate to desired locations
- Weather forecast
- Set remainders
- Sunrise and sunset forecast
- Turn On/Off Bluetooth
- Turn On/Off WI-FI
- Movie suggestions
- Conversational chatting
- Take screenshots
- Ask riddles
- Sing songs
- Recommand nearby places
- Sing poems
- Handsfree google search
- Calculations
- Store secrets
- Play games


## Appendix

To successfully execute this project, it is necessary to have your own API keys for accessing the required services. Additionally, a Python version equal to or higher than 11.0 is required. Furthermore, to ensure secure decryption, you will need to obtain a security key that will be used for the decryption process. These prerequisites are essential for the proper functioning and security of the project.


## Documentation

[Documentation](#)

