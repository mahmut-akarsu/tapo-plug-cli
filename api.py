from fastapi import FastAPI, HTTPException

from tapo_plug import TapoConfigError, TapoConnectionError, TapoPlug, get_plug_config, load_plugs_from_env

app = FastAPI(title="Tapo Plug API")


def _plug(plug_id: str) -> TapoPlug:
    try:
        return TapoPlug(config=get_plug_config(plug_id))
    except TapoConfigError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/plugs")
def list_plugs():
    try:
        plugs = load_plugs_from_env()
    except TapoConfigError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"plugs": sorted(plugs.keys())}


@app.post("/on/{plug_id}")
def on(plug_id: str):
    try:
        _plug(plug_id).on()
    except TapoConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"ok": True, "action": "on", "plug_id": plug_id}


@app.post("/off/{plug_id}")
def off(plug_id: str):
    try:
        _plug(plug_id).off()
    except TapoConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"ok": True, "action": "off", "plug_id": plug_id}
