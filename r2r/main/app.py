from fastapi import FastAPI

from .engine import R2REngine


class R2RApp:

    fastapi: FastAPI

    def __init__(self, engine: R2REngine):
        self.engine = engine
        self._setup_routes()
        self._apply_cors()

    async def openapi_spec(self, *args, **kwargs):
        from fastapi.openapi.utils import get_openapi

        return get_openapi(
            title="R2R Application API",
            version="1.0.0",
            routes=self.fastapi.routes,
        )

    def _setup_routes(self):
        from .api.routes import ingestion, management, retrieval

        self.fastapi = FastAPI()

        # Create routers with the engine
        ingestion_router = ingestion.create_ingestion_router(self.engine)
        management_router = management.create_management_router(self.engine)
        retrieval_router = retrieval.create_retrieval_router(self.engine)

        # Include routers in the app
        self.fastapi.include_router(ingestion_router, prefix="/v1")
        self.fastapi.include_router(management_router, prefix="/v1")
        self.fastapi.include_router(retrieval_router, prefix="/v1")

    def _apply_cors(self):
        from fastapi.middleware.cors import CORSMiddleware

        origins = ["*", "http://localhost:3000", "http://localhost:8000"]
        self.fastapi.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def serve(self, host: str = "0.0.0.0", port: int = 8000):
        import uvicorn

        print("real start")
        loggers = uvicorn.config.LOGGING_CONFIG["loggers"]

        uvicorn.run(self.fastapi, host=host, port=port, reload=True)
