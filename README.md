# Hide

> Version 1.0.0

Hide API

## Path Table

| Method | Path | Description |
| --- | --- | --- |
| GET | [/api/v1/user](#getapiv1user) | Get User List |
| POST | [/api/v1/user](#postapiv1user) | Create User |
| POST | [/api/v1/user/login](#postapiv1userlogin) | Login |
| POST | [/api/v1/auth/refresh](#postapiv1authrefresh) | Refresh Token |
| POST | [/api/v1/auth/verify](#postapiv1authverify) | Verify Token |
| POST | [/upload](#postupload) | Upload Audio |
| GET | [/download/{file_name}/{original_file_name}](#getdownloadfile_nameoriginal_file_name) | Download File |
| GET | [/list_user_audio](#getlist_user_audio) | List User Audio |
| GET | [/search](#getsearch) | Search Audio |
| GET | [/](#get) | Read Root |
| GET | [/login](#getlogin) | Read Root |
| GET | [/list](#getlist) | Read Root |

## Reference Table

| Name | Path | Description |
| --- | --- | --- |
| AudioFileRead | [#/components/schemas/AudioFileRead](#componentsschemasaudiofileread) |  |
| AudioUploadResponseDTO | [#/components/schemas/AudioUploadResponseDTO](#componentsschemasaudiouploadresponsedto) |  |
| Body_upload_audio_upload_post | [#/components/schemas/Body_upload_audio_upload_post](#componentsschemasbody_upload_audio_upload_post) |  |
| CreateUserRequest | [#/components/schemas/CreateUserRequest](#componentsschemascreateuserrequest) |  |
| CreateUserResponseDTO | [#/components/schemas/CreateUserResponseDTO](#componentsschemascreateuserresponsedto) |  |
| GetUserListResponseDTO | [#/components/schemas/GetUserListResponseDTO](#componentsschemasgetuserlistresponsedto) |  |
| HTTPValidationError | [#/components/schemas/HTTPValidationError](#componentsschemashttpvalidationerror) |  |
| LoginRequest | [#/components/schemas/LoginRequest](#componentsschemasloginrequest) |  |
| RefreshTokenRequest | [#/components/schemas/RefreshTokenRequest](#componentsschemasrefreshtokenrequest) |  |
| RefreshTokenResponse | [#/components/schemas/RefreshTokenResponse](#componentsschemasrefreshtokenresponse) |  |
| UserAudioResponse | [#/components/schemas/UserAudioResponse](#componentsschemasuseraudioresponse) |  |
| UserAudioType | [#/components/schemas/UserAudioType](#componentsschemasuseraudiotype) |  |
| ValidationError | [#/components/schemas/ValidationError](#componentsschemasvalidationerror) |  |
| VerifyTokenRequest | [#/components/schemas/VerifyTokenRequest](#componentsschemasverifytokenrequest) |  |
| PermissionDependency | [#/components/securitySchemes/PermissionDependency](#componentssecurityschemespermissiondependency) |  |

## Path Details

***

### [GET]/api/v1/user

- Summary  
Get User List

- Security  
PermissionDependency  

#### Parameters(Query)

```ts
// Limit
limit?: integer //default: 10
```

```ts
// Prev ID
prev?: integer
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  // ID
  id: integer
  // Email
  email: string
  // Nickname
  nickname: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/api/v1/user

- Summary  
Create User

#### RequestBody

- application/json

```ts
{
  // Nickname
  nickname: string
  // Password1
  password: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  // Email
  email: string
  // Nickname
  nickname: string
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/api/v1/user/login

- Summary  
Login

#### RequestBody

- application/json

```ts
{
  // Nickname
  nickname: string
  // Password
  password: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/api/v1/auth/refresh

- Summary  
Refresh Token

#### RequestBody

- application/json

```ts
{
  // Token
  token: string
  // Refresh token
  refresh_token: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  // Token
  token: string
  // Refresh token
  refresh_token: string
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/api/v1/auth/verify

- Summary  
Verify Token

#### RequestBody

- application/json

```ts
{
  // Token
  token: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/upload

- Summary  
Upload Audio

- Security  
PermissionDependency  

#### RequestBody

- multipart/form-data

```ts
{
  file: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  // task_id
  task_id: string
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/download/{file_name}/{original_file_name}

- Summary  
Download File

#### Parameters(Query)

```ts
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/list_user_audio

- Summary  
List User Audio

- Security  
PermissionDependency  

#### Parameters(Query)

```ts
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  audio_types: {
    id: string
    ext: string
    file_type: string
    file_size_in_bytes: integer
  }[]
  base_name: string
  nickname: string
  length_in_seconds: integer
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/search

- Summary  
Search Audio

- Security  
PermissionDependency  

#### Parameters(Query)

```ts
// Search query
q: string
```

```ts
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  user_id: integer
  original_file_name: string
  file_name: string
  created_at: string
  nickname: string
  file_size_in_bytes: integer
  length_in_seconds: integer
  file_type: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/

- Summary  
Read Root

#### Responses

- 200 Successful Response

`text/html`

```ts
{
  "type": "string"
}
```

***

### [GET]/login

- Summary  
Read Root

#### Responses

- 200 Successful Response

`text/html`

```ts
{
  "type": "string"
}
```

***

### [GET]/list

- Summary  
Read Root

#### Responses

- 200 Successful Response

`text/html`

```ts
{
  "type": "string"
}
```

## References

### #/components/schemas/AudioFileRead

```ts
{
  user_id: integer
  original_file_name: string
  file_name: string
  created_at: string
  nickname: string
  file_size_in_bytes: integer
  length_in_seconds: integer
  file_type: string
}
```

### #/components/schemas/AudioUploadResponseDTO

```ts
{
  // task_id
  task_id: string
}
```

### #/components/schemas/Body_upload_audio_upload_post

```ts
{
  file: string
}
```

### #/components/schemas/CreateUserRequest

```ts
{
  // Nickname
  nickname: string
  // Password1
  password: string
}
```

### #/components/schemas/CreateUserResponseDTO

```ts
{
  // Email
  email: string
  // Nickname
  nickname: string
}
```

### #/components/schemas/GetUserListResponseDTO

```ts
{
  // ID
  id: integer
  // Email
  email: string
  // Nickname
  nickname: string
}
```

### #/components/schemas/HTTPValidationError

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

### #/components/schemas/LoginRequest

```ts
{
  // Nickname
  nickname: string
  // Password
  password: string
}
```

### #/components/schemas/RefreshTokenRequest

```ts
{
  // Token
  token: string
  // Refresh token
  refresh_token: string
}
```

### #/components/schemas/RefreshTokenResponse

```ts
{
  // Token
  token: string
  // Refresh token
  refresh_token: string
}
```

### #/components/schemas/UserAudioResponse

```ts
{
  audio_types: {
    id: string
    ext: string
    file_type: string
    file_size_in_bytes: integer
  }[]
  base_name: string
  nickname: string
  length_in_seconds: integer
}
```

### #/components/schemas/UserAudioType

```ts
{
  id: string
  ext: string
  file_type: string
  file_size_in_bytes: integer
}
```

### #/components/schemas/ValidationError

```ts
{
  loc?: Partial(string) & Partial(integer)[]
  msg: string
  type: string
}
```

### #/components/schemas/VerifyTokenRequest

```ts
{
  // Token
  token: string
}
```

### #/components/securitySchemes/PermissionDependency

```ts
{
  "type": "apiKey",
  "in": "header",
  "name": "Authorization"
}
```