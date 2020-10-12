FROM node
WORKDIR .
COPY package.json .
RUN npm install
RUN npm install express
COPY . .
CMD node app.js
EXPOSE 5000