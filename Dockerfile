FROM python:3.9

WORKDIR /app

ENV DATABASE_URL=postgresql://desafio_782f_user:HetMfgdmmDQXXxfQIE2Bd589FxElotNm@dpg-cne1bsun7f5s73bnj080-a.oregon-postgres.render.com/desafio_782f

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
EXPOSE 5432

CMD ["flask", "run", "--host=0.0.0.0"]
